from app.config_reader import config
from app.infrastructure.workflow.celery import celery
from app.infrastructure.workflow.tasks.check_delivery_task import check_delivery_expire_task
from app.infrastructure.workflow.tasks.script_task import update_orders_task
from celery.schedules import crontab


@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(config.UPDATE_TIMEOUT, update_orders_task.s(), name="update_orders")

    sender.add_periodic_task(
        crontab(hour=9, minute=0), check_delivery_expire_task.s(), name="check_delivery_expire_task"
    )
