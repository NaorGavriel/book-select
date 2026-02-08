import time
from app.celery_app import celery_app

@celery_app.task
def example_task(job_id: int):
    time.sleep(5)
    print(f"Processed job {job_id}")
    return job_id
