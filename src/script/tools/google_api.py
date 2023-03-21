
import gspread

from src.config_reader import config

WORKSHEET_ID = 0


def create_client() -> gspread.Client:
    client = gspread.service_account_from_dict(
        info=config.GSAPI_SERVICE_KEY.dict())
    return client


def get_spreadsheet() -> gspread.Spreadsheet:
    client = create_client()
    spreadsheet = client.open_by_key(config.GSAPI_ID)
    return spreadsheet


def get_worksheet(worksheet_id: int) -> gspread.Worksheet:
    spreadsheet = get_spreadsheet()
    worksheet = spreadsheet.get_worksheet(worksheet_id)
    return worksheet

