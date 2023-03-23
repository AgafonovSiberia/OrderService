import gspread

from app.config_reader import config
from gspread.client import BackoffClient
from gspread.auth import ServiceAccountCredentials, DEFAULT_SCOPES
from functools import lru_cache


def create_client() -> gspread.Client:
    """
    Инициализирует клиент для доступа к гугл-таблице
    BackoffClient расширение gspread.Client, поддерживающее
    retry-функционал в случае получения GoogleAPIError
    :return: gspread.BackoffClient
    """
    cred = ServiceAccountCredentials.from_service_account_info(
        info=config.GSAPI_SERVICE_KEY.dict(), scopes=DEFAULT_SCOPES
    )
    client = BackoffClient(auth=cred)
    return client


def get_spreadsheet() -> gspread.Spreadsheet:
    """
    Получает объект 'Книга'
    Параметры для config.GSAPI_ID можно узнать
    из URL .../spreadsheets/d/"spreadsheet_id"/...
    """
    client = create_client()
    spreadsheet = client.open_by_key(config.GSAPI_ID)
    return spreadsheet


@lru_cache
def get_worksheet(worksheet_id: int) -> gspread.Worksheet:
    """
    Получает объект 'РабочийЛист'
    :param worksheet_id: ID-листа в текущей книге (нумерация с 0)
    Можно узнать из URL ...#gid="list index"
    """
    spreadsheet = get_spreadsheet()
    worksheet = spreadsheet.get_worksheet(worksheet_id)
    return worksheet
