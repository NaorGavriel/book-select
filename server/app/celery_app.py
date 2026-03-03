import os
from celery import Celery

REDIS_URL = os.environ.get("REDIS_JOBS_URL")

celery_app = Celery(
    "bookselect",
    broker=REDIS_URL,
    backend=REDIS_URL,
)

celery_app.autodiscover_tasks(["app.job_tasks"])
