import os
from celery import Celery
from app.core.logger.logger import init_logging


REDIS_URL = os.environ.get("REDIS_JOBS_URL")

init_logging()

celery_app = Celery(
    "bookselect",
    broker=REDIS_URL,
    backend=REDIS_URL,
)

celery_app.autodiscover_tasks(["app.job_tasks"])
