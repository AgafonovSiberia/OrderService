from app.infrastructure.repo.orders import OrderRepo
from app.infrastructure.workflow.celery import celery
from app.infrastructure.workflow.database_task import DatabaseTask
from app.services.ext_api import emailing_to_admins
from app.services.ext_api import render_message_order_expire
from celery.app import task


@celery.task(base=DatabaseTask, bind=True)
def check_delivery_expire_task(self: task):
    repo = self.repo
    expire_orders_list = repo.get_repo(OrderRepo).get_expire_orders()

    message = render_message_order_expire(expire_orders_list)
    emailing_to_admins(message=message)
