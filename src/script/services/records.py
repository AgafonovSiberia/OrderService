from src.script.tools.google_api import get_worksheet
from src.script.schemas import RecordSchema
from src.script.tools.current_rate import get_current_rate_from_api
from src.infrastucture.db.factory import create_pool
from src.infrastucture.repo.record import RecordRepo

WORKSHEET_ID = 0


def get_records_from_sheets() -> list[RecordSchema]:
    """
    Получает все записи из GoogleSheet, приводит к list[object Record]
    :return: list[Record]

    !! Надо обрабатывать ошибки гугла (смотреть лимиты)
    """
    ws = get_worksheet(WORKSHEET_ID)
    values_list = ws.get_all_records()
    list_records: list[RecordSchema] = [
        RecordSchema(**record_row) for record_row in values_list
    ]
    return list_records


def update_record_to_database():
    list_records: list[RecordSchema] = get_records_from_sheets()
    current_rate = get_rate_usb_to_rub()

    pool = create_pool()
    with pool() as session:
        repo = RecordRepo(session)
        for record in list_records:
            repo.add_record(record, current_rate)


def get_rate_usb_to_rub():
    return get_current_rate_from_api()
