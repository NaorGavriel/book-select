"""
Background job processing tasks.

This module contains Celery tasks responsible for executing long-running
job workloads and updating job lifecycle state.
"""

from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.crud.jobs import get_job_by_id, update_job_status
from app.models.enums import JobStatus
from app.celery_app import celery_app
import time


@celery_app.task
def process_job(job_id: int):
    """
    Execute an image-processing job.

    Updates job status as it progresses and records failure details
    if an exception occurs.
    """
    db: Session = SessionLocal()
    job = None

    try:
        job = get_job_by_id(db, job_id)
        if job is None:
            return

        if job.status != JobStatus.pending: # preventing double-exec of the job by checking status
            return


        update_job_status(db, job, status=JobStatus.processing)

        time.sleep(5) # simulating proceesing until implementation

        update_job_status(db, job, status=JobStatus.completed)

    except Exception as e:
        if job is not None:
            update_job_status(db, job, status=JobStatus.failed, error_message=str(e))
        raise

    finally:
        db.close()
