"""
Metrics aggregation service.

Queries PostgreSQL and Redis to assemble a snapshot of system health,
recommendation quality, performance, and user growth.
"""
from datetime import datetime, timedelta, timezone

import redis as redis_lib
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.book import Book
from app.models.enums import Decision, JobStatus
from app.models.job_result import JobResult
from app.models.jobs import Job
from app.models.user import User
from app.models.user_book import UserBook
from app.schemas.metrics import (
    AuthorCount,
    BookCount,
    CacheMetrics,
    GenreCount,
    JobMetrics,
    MetricsResponse,
    PerformanceMetrics,
    RecommendationMetrics,
    UserMetrics,
)

_TOP_N = 10


def _get_cache_metrics(rc: redis_lib.Redis) -> CacheMetrics:
    """Read cumulative cache hit/miss counters from Redis and compute the hit rate."""
    hits = int(rc.get("metrics:cache:hits") or 0)
    misses = int(rc.get("metrics:cache:misses") or 0)
    total = hits + misses
    hit_rate = round(hits / total, 4) if total > 0 else 0.0
    return CacheMetrics(hits=hits, misses=misses, hit_rate=hit_rate)


def _get_job_metrics(db: Session, today: datetime) -> JobMetrics:
    """Count jobs created today and totals by terminal status."""
    total_today = db.query(func.count(Job.id)).filter(Job.created_at >= today).scalar() or 0

    status_rows = (
        db.query(Job.status, func.count(Job.id).label("cnt"))
        .group_by(Job.status)
        .all()
    )
    status_map = {row.status: row.cnt for row in status_rows}

    return JobMetrics(
        total_today=total_today,
        completed=status_map.get(JobStatus.completed, 0),
        failed=status_map.get(JobStatus.failed, 0),
    )


def _get_recommendation_metrics(db: Session, today: datetime, week_start: datetime) -> RecommendationMetrics:
    """Aggregate recommendation counts, confidence averages, decision splits, and top lists."""
    total, today_count, this_week = db.query(
        func.count(JobResult.id),
        func.count(JobResult.id).filter(JobResult.created_at >= today),
        func.count(JobResult.id).filter(JobResult.created_at >= week_start),
    ).one()
    total = total or 0

    avg_confidence = round(float(db.query(func.avg(JobResult.confidence)).scalar() or 0.0), 4)

    decision_rows = (
        db.query(JobResult.decision, func.count(JobResult.id).label("cnt"))
        .group_by(JobResult.decision)
        .all()
    )
    decision_map = {row.decision: row.cnt for row in decision_rows}

    def _pct(key: Decision) -> float:
        """Compute percentage share of a single decision type."""
        if total == 0:
            return 0.0
        return round(decision_map.get(key, 0) / total * 100, 2)

    top_books = [
        BookCount(title=row.title, count=row.count)
        for row in db.query(JobResult.title, func.count(JobResult.id).label("count"))
        .group_by(JobResult.title)
        .order_by(func.count(JobResult.id).desc())
        .limit(_TOP_N)
        .all()
    ]

    author_col = func.jsonb_array_elements_text(JobResult.authors).column_valued("author")
    top_authors = [
        AuthorCount(author=row.author, count=row.count)
        for row in (
            db.query(author_col, func.count().label("count"))
            .select_from(JobResult)
            .group_by(author_col)
            .order_by(func.count().desc())
            .limit(_TOP_N)
            .all()
        )
    ]

    genre_col = func.jsonb_array_elements_text(Book.genres).column_valued("genre")
    top_genres = [
        GenreCount(genre=row.genre, count=row.count)
        for row in (
            db.query(genre_col, func.count().label("count"))
            .select_from(JobResult)
            .join(Book, func.lower(Book.title) == func.lower(JobResult.title))
            .group_by(genre_col)
            .order_by(func.count().desc())
            .limit(_TOP_N)
            .all()
        )
    ]

    return RecommendationMetrics(
        total=total,
        today=today_count,
        this_week=this_week,
        avg_confidence=avg_confidence,
        strong_match_pct=_pct(Decision.strong_match),
        consider_pct=_pct(Decision.consider),
        avoid_pct=_pct(Decision.avoid),
        top_books=top_books,
        top_authors=top_authors,
        top_genres=top_genres,
    )


def _get_performance_metrics(db: Session, rc: redis_lib.Redis) -> PerformanceMetrics:
    """Compute average cache lookup latency from Redis and average job duration from the DB."""
    latency_sum = float(rc.get("metrics:cache:lookup_latency_ms_sum") or 0)
    lookup_count = int(rc.get("metrics:cache:lookup_count") or 0)
    avg_cache_latency = round(latency_sum / lookup_count, 3) if lookup_count > 0 else 0.0

    avg_duration = float(
        db.query(
            func.avg(func.extract("epoch", Job.completed_at - Job.created_at))
        )
        .filter(Job.status == JobStatus.completed, Job.completed_at.isnot(None))
        .scalar()
        or 0.0
    )

    return PerformanceMetrics(
        avg_cache_lookup_latency_ms=avg_cache_latency,
        avg_job_processing_duration_s=round(avg_duration, 3),
    )


def _get_user_metrics(db: Session, today: datetime) -> UserMetrics:
    """Count total, active, new, and reading-history users."""
    total = db.query(func.count(User.id)).scalar() or 0
    thirty_days_ago = datetime.now(timezone.utc) - timedelta(days=30)
    active = (
        db.query(func.count(func.distinct(Job.user_id)))
        .filter(Job.created_at >= thirty_days_ago)
        .scalar()
        or 0
    )
    new_today = (
        db.query(func.count(User.id))
        .filter(User.created_at >= today)
        .scalar()
        or 0
    )
    reading_history_count = db.query(func.count()).select_from(UserBook).scalar() or 0
    return UserMetrics(
        total=total,
        active=active,
        new_today=new_today,
        reading_history_count=reading_history_count,
    )


def get_all_metrics(db: Session, rc: redis_lib.Redis) -> MetricsResponse:
    """Assemble a full metrics snapshot from PostgreSQL and Redis."""
    now = datetime.now(timezone.utc)
    today = now.replace(hour=0, minute=0, second=0, microsecond=0)
    week_start = today - timedelta(days=today.weekday())

    return MetricsResponse(
        cache=_get_cache_metrics(rc),
        jobs=_get_job_metrics(db, today),
        recommendations=_get_recommendation_metrics(db, today, week_start),
        performance=_get_performance_metrics(db, rc),
        users=_get_user_metrics(db, today),
    )
