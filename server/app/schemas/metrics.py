from pydantic import BaseModel


class BookCount(BaseModel):
    """A book title paired with the number of times it appeared in recommendations."""
    title: str
    count: int


class AuthorCount(BaseModel):
    """An author name paired with the number of times they appeared in recommendations."""
    author: str
    count: int


class GenreCount(BaseModel):
    """A genre paired with the number of times it appeared in recommendations."""
    genre: str
    count: int


class CacheMetrics(BaseModel):
    """Book-cache hit and miss statistics stored in Redis."""
    hits: int
    misses: int
    hit_rate: float


class JobMetrics(BaseModel):
    """Job counts broken down by recency and final status."""
    total_today: int
    completed: int
    failed: int


class RecommendationMetrics(BaseModel):
    """Aggregated statistics about generated book recommendations."""
    total: int
    today: int
    this_week: int
    avg_confidence: float
    strong_match_pct: float
    consider_pct: float
    avoid_pct: float
    top_books: list[BookCount]
    top_authors: list[AuthorCount]
    top_genres: list[GenreCount]


class PerformanceMetrics(BaseModel):
    """Latency and throughput measurements for key operations."""
    avg_cache_lookup_latency_ms: float
    avg_job_processing_duration_s: float


class UserMetrics(BaseModel):
    """User growth and engagement statistics."""
    total: int
    active: int
    new_today: int
    reading_history_count: int


class MetricsResponse(BaseModel):
    """Top-level response containing all system metric categories."""
    cache: CacheMetrics
    jobs: JobMetrics
    recommendations: RecommendationMetrics
    performance: PerformanceMetrics
    users: UserMetrics
