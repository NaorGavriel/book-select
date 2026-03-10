from fastapi import APIRouter, Depends, HTTPException, Request, Response
from app.schemas.job_results import JobResultItem
from app.models.user import User
from sqlalchemy.orm import Session
from app.db import get_db
from app.services.job_results import get_job_results, get_all_results_for_user
from app.services.auth import get_current_user
from app.core.rate_limit.limiter import limiter

router = APIRouter(prefix="/results", tags=["results"])

@router.get("/{job_id}", response_model=list[JobResultItem])
@limiter.limit("5/minute")
def get_results(request : Request ,job_id: int, db: Session = Depends(get_db), user : User = Depends(get_current_user)):
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
        results = get_job_results(user.id, job_id, db)
        return results
    except ValueError:
        raise HTTPException(status_code=404, detail="Results not found")
    
@router.get("/", response_model=list[JobResultItem])
@limiter.limit("5/minute")
def get_all_results(request : Request, db: Session = Depends(get_db), user : User = Depends(get_current_user)):
    """
    Retrieve all results for a specific user.

    Args:
        user_id: Owner of the job.

    Returns:
        A list of job result items.

    Raises:
        HTTPException(404): If no results are found.
    """
    try:
        results = get_all_results_for_user(user.id, db)
        return results
    except ValueError:
        raise HTTPException(status_code=404, detail="Results not found")
