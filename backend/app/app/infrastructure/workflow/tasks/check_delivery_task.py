from app.infrastructure.repo import OrderRepo
from app.infrastructure.workflow.celery import celery
from app.infrastructure.workflow.database_task import DatabaseTask
from app.services.ext_api import emailing_to_admins
from app.services.ext_api import render_message_order_expire
from celery.app import task


@celery.task(base=DatabaseTask, bind=True)
def check_delivery_expire_task(self: task) -> None:
    """
    Проверяет, есть ли в БД заказы срок поставки которых истекает сегодня.
    Если такие заказы есть, то отправляет сообщение в Telegram.
    :param self: имплементация задачи (весь сохранённый контекст и базовый
    класс DatabaseTask, предоставляющий достук к БД)
    """
    expire_orders_list = self.repo.get_repo(OrderRepo).get_expire_orders()

    message = render_message_order_expire(expire_orders_list)
    emailing_to_admins(message=message)
