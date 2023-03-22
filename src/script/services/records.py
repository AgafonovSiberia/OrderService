from src.script.tools.google_api import get_worksheet
from src.script.schemas import RecordSchema
from src.script.tools.current_rate import get_current_rate_from_api
from src.infrastucture.repo.record_repo import RecordRepo

from src.infrastucture.repo.base.repository import get_base_repo
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy import event

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


def update_record_to_database(pool: sessionmaker) -> None:
    """
    Обновляет записи из GoogleSheet в БД.
    Считает значение для поля цена в рублях.
    :param pool: Пул соединений с БД
    """
    list_records: list[RecordSchema] = get_records_from_sheets()
    current_rate = get_current_rate_from_api()

    with pool() as _session:
        event.listen(_session, "after_commit", receive_after_flush)

        repo = get_base_repo(_session).get_repo(RecordRepo)
        repo.add_records(records_list=list_records, rate=current_rate)


def receive_after_flush(session):
    print("Тут дернем вебсокет для реакта")
