from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from app.db import get_db
from app.services.jobs import create_job_from_image

router = APIRouter(prefix="/jobs", tags=["jobs"])

@router.post("")
async def post_job(file: UploadFile = File(...), db: Session = Depends(get_db), user_id: int = 1):
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