from src.script.schemas import RecordSchema
from src.script.services.current_rate import get_current_rate_from_api
from src.infrastucture.repo.record_repo import RecordRepo
from src.script.services.google_api import get_worksheet
from src.infrastucture.repo.base.repository import get_base_repo
from sqlalchemy import event

from src.logger import logger
from src.utils import timeit

WORKSHEET_ID = 0


@timeit
def get_records_from_sheets() -> list[RecordSchema]:
    """
    Получает все записи из GoogleSheet, приводит к list[object Record]
    :return: list[Record]
    """

    ws = get_worksheet(WORKSHEET_ID)
    values_list = ws.get_all_records()

    list_records: list[RecordSchema] = [
        RecordSchema(**record_row) for record_row in values_list
    ]
    return list_records


@timeit
def update_record_to_database(pool) -> None:
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
    # тут будем дергать вебсокет для реакта
    logger.info("Session committed")
