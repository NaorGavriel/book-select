from celery import Celery
from app.core.logger.logger import init_logging
from app.core.config import GeneralConfig
from celery.signals import setup_logging


celery_app = Celery(
    "bookselect",
    broker=GeneralConfig.REDIS_JOB_URL,
    backend=GeneralConfig.REDIS_JOB_URL,
)

celery_app.autodiscover_tasks(["app.job_tasks"])

@setup_logging.connect
def config_loggers(*args, **kwargs):
    init_logging()