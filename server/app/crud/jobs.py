from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.jobs import Job
from app.models.enums import JobStatus

"""
Database operations for Job records.
"""
def create_job(db: Session,user_id: int, image_path: str) -> Job:
    """
    creates a new job in pending state.
    """
    job = Job(
        user_id=user_id,
        image_path=image_path,
        status=JobStatus.pending,
    )

    db.add(job)
    db.commit()
    db.refresh(job)
    return job


def get_job_by_id(db: Session, job_id: int, user_id: int) -> Job | None:
    """
    Fetch a job by job_id (PK) and user_id.
    """
    return db.query(Job).filter(Job.id == job_id, Job.user_id == user_id).first()


def update_job_status(db: Session, job: Job, *, status: JobStatus, error_message: str | None = None) -> Job:
    """
    Update job status, completion metadata, optional error message.
    """
    job.status = status
    job.error_message = error_message

    if status in (JobStatus.completed, JobStatus.failed):
        job.completed_at = func.now()

    db.commit()
    db.refresh(job)
    return job
