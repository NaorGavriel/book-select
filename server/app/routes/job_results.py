from fastapi import APIRouter, Depends, HTTPException
from app.schemas.job_results import JobResultItem

from sqlalchemy.orm import Session
from app.db import get_db
from app.services.job_results import get_job_results

router = APIRouter(prefix="/results", tags=["results"])

@router.get("/{job_id}", response_model=list[JobResultItem])
def get_results(user_id: int, job_id: int, db: Session = Depends(get_db)):
    """
    Retrieve all results for a specific job.

    Args:
        user_id: Owner of the job.
        job_id: Identifier of the job.

    Returns:
        A list of job result items for the given job.

    Raises:
        HTTPException(404): If no results are found for the job.
    """
    try:
        results = get_job_results(user_id, job_id, db)
        return results
    except ValueError:
        raise HTTPException(status_code=404, detail="Results not found")
