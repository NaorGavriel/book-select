from sqlalchemy.orm import Session
from app.models.job_result import JobResult
from app.models.enums import Decision
from app.dto.book_result import BookResult

def create_job_result(db: Session, book_result : BookResult, job_id : int) -> JobResult:
    """
    Create and a job result record.

    The record is added to the current database session but is not
    committed. Transaction boundaries are managed by the caller.

    Args:
        db: Active SQLAlchemy session.
        user_id: Owner of the job.
        job_id: Job ID
        title: Book title.
        authors: List of author names.
        decision: Match decision outcome.
        confidence: Confidence score in the range [0, 1].
        explanation: Explanation of the decision.

    Returns:
        The created JobResult ORM instance.
    """
    result = JobResult(
        user_id=book_result.user_id,
        job_id=job_id,
        title=book_result.title,
        authors=book_result.authors,
        decision=book_result.decision,
        confidence=book_result.confidence,
        explanation=book_result.explanation,
    )

    db.add(result)
    return result

def get_results(db: Session,user_id: int, job_id: int):
    """
    Retrieve all results for a specific job and user.

    Args:
        db: Active SQLAlchemy session.
        user_id: Owner of the job.
        job_id: Identifier of the job.

    Returns:
        A list of JobResult records matching the job and user.
    """
    results = db.query(JobResult).filter(JobResult.job_id == job_id, JobResult.user_id == user_id).all()
    return results

def get_all_results(db: Session,user_id: int):
    """
    Retrieve all results for a specific user.

    Args:
        db: Active SQLAlchemy session.
        user_id: Owner of the job.

    Returns:
        A list of JobResult records matching the user.
    """
    results = db.query(JobResult).filter(JobResult.user_id == user_id).order_by(JobResult.created_at.desc()).all()
    return results