from sqlalchemy.orm import Session
from app.crud.job_results import get_results, get_all_results
from app.models.job_result import JobResult

def get_job_results(user_id:int ,job_id: int, db: Session):
    """
    Retrieve job results for a specific user and job.

    Args:
        user_id: Owner of the job.
        job_id: Identifier of the job.
        db: Active SQLAlchemy session.

    Returns:
        A list of job result records associated with the given job.

    Raises:
        ValueError: If no results are found for the job.
    """
    results = get_results(db, user_id, job_id)
    if results == []:
            raise ValueError
    return results

def get_all_results_for_user(user_id:int, db: Session) -> list[JobResult]:
    """
    Retrieve all results for a specific user.

    Args:
        user_id: Owner of the job.
        db: Active SQLAlchemy session.

    Returns:
        A list of job result records associated with the given user_id

    Raises:
        ValueError: If no results are found for the job.
    """
    results = get_all_results(db, user_id)
    if results == []:
            raise ValueError
    return results