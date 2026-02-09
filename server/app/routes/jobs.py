from fastapi import APIRouter,HTTPException, Depends, UploadFile, File
from sqlalchemy.orm import Session
from app.db import get_db
from app.services.jobs import create_job_from_image, get_job

router = APIRouter(prefix="/jobs", tags=["jobs"])

@router.post("")
async def post_job(file: UploadFile = File(...), db: Session = Depends(get_db), user_id: int = 1):
    """
    Posts new image-processing job.

    Returns immediately with job_id for polling.
    """
    image_bytes = await file.read()

    job = create_job_from_image(
        user_id=user_id,
        image_bytes=image_bytes,
        filename=file.filename,
        db=db,
    )

    return {
        "job_id": job.id,
        "status": job.status,
    }

@router.get("/{job_id}")
def get_job_status(job_id: int, db: Session = Depends(get_db)):
    """
    Retrieve the current status of a job.
    """
    try:
        job = get_job(job_id, db)
    except ValueError:
        raise HTTPException(status_code=404, detail="Job not found")

    return {
        "job_id": job.id,
        "status": job.status,
        "error_message": job.error_message,
        "completed_at": job.completed_at,
    }