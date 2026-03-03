from fastapi import APIRouter,HTTPException, Depends, UploadFile, File
from sqlalchemy.orm import Session
from app.db import get_db
from app.services.jobs import create_job_from_image, get_job
from app.models.user import User
from app.services.auth import get_current_user
router = APIRouter(prefix="/jobs", tags=["jobs"])

@router.post("")
async def post_job(file: UploadFile = File(...), db: Session = Depends(get_db), user : User = Depends(get_current_user)):
    """
    Posts new image-processing job.

    Returns immediately with job_id for polling.
    """
    image_bytes = await file.read()

    job = create_job_from_image(
        user_id=user.id,
        image_bytes=image_bytes,
        filename=file.filename,
        db=db,
    )

    return {
        "job_id": job.id,
        "status": job.status,
    }

@router.get("/{job_id}")
def get_job_status(job_id: int, db: Session = Depends(get_db), user : User = Depends(get_current_user)):
    """
    Retrieve the current status of a job.
    """
    try:
        job = get_job(user_id=user.id, job_id=job_id, db=db)
    except ValueError:
        raise HTTPException(status_code=404, detail="Job not found")

    return {
        "job_id": job.id,
        "status": job.status,
        "error_message": job.error_message,
        "completed_at": job.completed_at,
    }