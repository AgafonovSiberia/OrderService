import gspread

from src.config_reader import config




def create_client() -> gspread.Client:
    """ Инициализация клиента для доступа к гугл-таблице"""
    client = gspread.service_account_from_dict(
        info=config.GSAPI_SERVICE_KEY.dict())
    return client


def get_spreadsheet() -> gspread.Spreadsheet:
    """ Получает объект 'Книга' """
    client = create_client()
    spreadsheet = client.open_by_key(config.GSAPI_ID)
    return spreadsheet


def get_worksheet(worksheet_id: int) -> gspread.Worksheet:
    """
    Получает объект 'РабочийЛист'
    :param worksheet_id: ID-листа в текущей книге (нумерация с 0)
    Можно узнать из URL ...#gid="list index"
    """
    spreadsheet = get_spreadsheet()
    worksheet = spreadsheet.get_worksheet(worksheet_id)
    return worksheet

