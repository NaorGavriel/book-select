from sqlalchemy.orm import Session
from app.crud.jobs import create_job, get_job_by_id
#from app.tasks.jobs import process_job
from app.storage.storage_factory import get_storage_backend
from app.storage.storage_base import StorageBase
from app.models.jobs import Job

def create_job_from_image(user_id: int, image_bytes: bytes,filename: str,db: Session):
    """
    Create a new image-processing job from uploaded image data.

    Persists the image, creates a pending job record, and enqueues Celery task for job processing.
    """
    storage : StorageBase = get_storage_backend()

    # storing image
    image_path = storage.save_image(
        image_bytes=image_bytes,
        filename=filename,
        user_id=user_id,
    )

    # creating job entry in the database
    job = create_job(
        db = db,
        user_id = user_id,
        image_path = image_path,
    )

    # enqueing job processing task
    #process_job.delay(job.id)

    return job

def get_job(job_id: int, db: Session) -> Job:
    """
    Retrieve a job by job_id or raise ValueError if not found.
    """
    job = get_job_by_id(db, job_id)
    if job is None:
        raise ValueError("Job not found")
    return job
