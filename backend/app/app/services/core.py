from gspread import Worksheet

from app.services.schemas import OrderSchema, OrderFullSchema
from app.services.current_rate import get_current_rate_from_api
from app.infrastructure.repo.orders import OrderRepo
from app.services.google_api import get_worksheet
from app.infrastructure.repo.base.repository import get_base_repo
from sqlalchemy import event

from app.logger import logger
from app.utils import timeit

WORKSHEET_ID = 0


@timeit
def get_orders_from_sheets() -> list[OrderFullSchema]:
    """
    Получает все записи из GoogleSheet, приводит к list[PydanticModel - OrderSchema]
    :return: list[OrderSchema]
    """

    sheet: Worksheet = get_worksheet(WORKSHEET_ID)
    values_list = sheet.get_all_records()

    list_orders: list[OrderFullSchema] = [
        OrderFullSchema(**record_row) for record_row in values_list
    ]
    return list_orders


@timeit
def update_orders_to_database(pool) -> None:
    """
    Обновляет записи в БД.
    Считает значение для поля цена в рублях.
    :param pool: Пул соединений с БД
    """
    list_orders: list[OrderSchema] = get_orders_from_sheets()
    current_rate = get_current_rate_from_api()

    with pool() as _session:
        event.listen(_session, "after_commit", receive_after_flush)
        repo = get_base_repo(_session).get_repo(OrderRepo)
        repo.add_orders(orders_list=list_orders)


def receive_after_flush(session):
    # тут можно дёргать вебсокет для реакта
    logger.info("Session committed")
