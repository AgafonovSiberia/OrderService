from app.infrastructure.workflow.celery import celery
from app.infrastructure.workflow.database_task import DatabaseTask
from app.services.core import update_orders_to_database
from celery.app import task


@celery.task(base=DatabaseTask, bind=True)
def update_orders_task(self: task):
    update_orders_to_database(self.repo)
