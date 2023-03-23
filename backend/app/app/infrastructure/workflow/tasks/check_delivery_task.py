from app.infrastructure.workflow.celery import celery
from app.services.core import update_orders_to_database
from sqlalchemy.orm import sessionmaker
from app.infrastructure.db.factory import create_pool
from app.infrastructure.repo.base.repository import SQLALchemyRepo
from app.infrastructure.repo.orders import OrderRepo


@celery.task
def check_delivery_expire_task():
    pool: sessionmaker = create_pool()
    with pool() as _session:
        repo = SQLALchemyRepo(_session).get_repo(OrderRepo)
        expire_orders_list = repo.get_repo(OrderRepo).get_expire_orders()
        data = [order.to_dict for order in expire_orders_list]


def render_message(data: list[dict]):
    pass



