from app.config_reader import config
from celery import Celery


celery = Celery(
    "web",
    broker=config.REDIS_URL,
    backend=config.REDIS_URL,
    include=[
        "app.infrastructure.workflow.tasks.periodic",
        "app.infrastructure.workflow.tasks.script_task",
        "app.infrastructure.workflow.tasks.check_delivery_task",
    ],
)


class CeleryConfig:
    timezone = "Europe/Moscow"


celery.config_from_object(CeleryConfig)
