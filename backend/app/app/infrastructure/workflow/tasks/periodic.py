from app.infrastructure.workflow.celery import celery
from app.config_reader import config
from app.infrastructure.workflow.tasks.script_task import update_orders_task

@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        config.UPDATE_TIMEOUT,
        update_orders_task.s(),
        name="update_orders"
    )


