from app.infrastructure.db.factory import create_pool
from app.infrastructure.repo.base.repository import SQLALchemyRepo
from app.infrastructure.repo.orders import OrderRepo
from app.infrastructure.workflow.celery import celery
from services.ext_api.tg_bot import emailing_to_admins
from services.ext_api.tg_bot import render_message_order_expire
from sqlalchemy.orm import sessionmaker


@celery.task
def check_delivery_expire_task():
    pool: sessionmaker = create_pool()
    with pool() as _session:
        repo = SQLALchemyRepo(_session)
        expire_orders_list = repo.get_repo(OrderRepo).get_expire_orders()

    message = render_message_order_expire(expire_orders_list)
    emailing_to_admins(message=message)
