
from src.script.tools.google_api import get_worksheet
from src.script.schemas import Record
from src.script.tools.current_rate import get_rate


WORKSHEET_ID = 0


def get_records_from_sheets() -> list[Record]:
    """
    Получает все записи из GoogleSheet, приводит к list[object Record]
    :return: list[Record]

    !! Надо обрабатывать ошибки гугла (смотреть лимиты)
    """
    ws = get_worksheet(WORKSHEET_ID)
    values_list = ws.get_all_records()
    list_records: list[Record] = [Record(**record_row) for record_row in values_list]
    return list_records


def update_price_to_database():
    pass


def price_to_rub():
    pass


def get_rate_ruble():
    print(get_rate())





