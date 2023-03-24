from decimal import Decimal

from app.exceptions.rate_except import RateAPIError
from app.infrastructure.repo.base.repository import SQLALchemyRepo
from app.infrastructure.repo.orders import OrderRepo
from app.logger import logger
from app.services.ext_api import get_current_rate_from_api
from app.services.ext_api import get_worksheet
from app.services.schemas import OrderSchema
from app.utils import timeit
from gspread import Worksheet

WORKSHEET_ID = 0


@timeit
def get_orders_from_sheets() -> list[OrderSchema]:
    """
    Получает все записи из GoogleSheet, приводит к app.services.schema.OrderSchema
    :return: list[app.services.schema.OrderSchema]
    """

    sheet: Worksheet = get_worksheet(WORKSHEET_ID)
    values_list = sheet.get_all_records()

    list_orders: list[OrderSchema] = [OrderSchema(**record_row) for record_row in values_list]
    convert_prices_to_rubles(list_orders)
    return list_orders


def convert_prices_to_rubles(list_orders: list[OrderSchema]) -> None:
    """
    Заполняет поле "стоимость в рублях" на основании курса,
    полученного от API ЦБ РФ. В случае, если API не смогло вернуть
    актуальный курс - поле "стоимость в рублях" зануляется.
    Такой подход позволяет указать конечному пользователю,
    что в данный момент актуальные данные по курсу недоступны.

    :param list_orders: Список заказов (app.services.schema.OrderSchema)
    """
    try:
        rate = get_current_rate_from_api()
    except RateAPIError:
        rate = Decimal("0")

    for order in list_orders:
        order.price_in_rubles = order.price_in_dollars * rate


@timeit
def update_orders_to_database(repo: SQLALchemyRepo) -> None:
    """
    Обновляет записи в БД.
    :param repo:
    """
    list_orders: list[OrderSchema] = get_orders_from_sheets()
    repo.get_repo(OrderRepo).add_orders(orders_list=list_orders)


def receive_after_flush(session) -> None:
    """
    Триггер после коммита всех заказов в БД.
    В этом месте можно дёрнуть веб-сокет для фронта.
    :param session: SQLAlchemy-session
    """

    logger.info("Session committed")
