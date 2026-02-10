from sqlalchemy.orm import Session
from app.crud.job_results import get_results

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