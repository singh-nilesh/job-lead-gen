from celery import Celery
from app.core.config import Settings

celery_app = Celery(
    "job_queue",
    broker=Settings.CELERY_BROKER_URL,
    backend=Settings.CELERY_RESULT_BACKEND,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

celery_app.autodiscover_tasks(packages=["app.tasks"])