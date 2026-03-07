from fastapi import APIRouter,HTTPException, Depends, UploadFile, File, Request, status
from sqlalchemy.orm import Session
from app.db import get_db
from app.services.jobs import create_job_from_image, get_job
from app.models.user import User
from app.services.auth import get_current_user
from app.core.rate_limit.limiter import limiter
from app.utils.image import process_image
from PIL import UnidentifiedImageError
from starlette.concurrency import run_in_threadpool
from app.core.config import GeneralConfig

router = APIRouter(prefix="/jobs", tags=["jobs"])

@router.post("")
@limiter.limit("2/minute")
@limiter.limit("10/day")
async def post_job(request: Request, file: UploadFile = File(...), db: Session = Depends(get_db), user : User = Depends(get_current_user)):
    """
    Posts new image-processing job.

    Returns immediately with job_id for polling.
    """
    image_bytes = await file.read()
    if len(image_bytes) > GeneralConfig.MAX_IMAGE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Image larger than {GeneralConfig.MAX_IMAGE_SIZE/(1024*1024)} MB"
        )

    try: 
        processed_image_bytes = await run_in_threadpool(process_image, image_bytes)
    except UnidentifiedImageError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid Image. Please upload only JPEG or PNG."
        )    

    job = create_job_from_image(
        user_id=user.id,
        image_bytes=processed_image_bytes,
        filename=file.filename,
        db=db,
    )

    return {
        "job_id": job.id,
        "status": job.status,
    }

@router.get("/{job_id}")
@limiter.limit("20/minute")
def get_job_status(request : Request, job_id: int, db: Session = Depends(get_db), user : User = Depends(get_current_user)):
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