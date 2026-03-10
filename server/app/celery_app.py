from celery import Celery
from app.core.logger.logger import init_logging
from app.core.config.config import settings
from celery.signals import setup_logging


celery_app = Celery(
    "bookselect",
    broker=settings.REDIS_JOBS_URL,
    backend=settings.REDIS_JOBS_URL,
)

celery_app.autodiscover_tasks(["app.job_tasks"])

@setup_logging.connect
def config_loggers(*args, **kwargs):
    init_logging()