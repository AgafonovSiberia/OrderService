from app.infrastructure.workflow.celery import celery
from app.services.core import update_orders_to_database
from sqlalchemy.orm import sessionmaker
from app.infrastructure.db.factory import create_pool


@celery.task
def update_orders_task():
    pool: sessionmaker = create_pool()
    update_orders_to_database(pool)


