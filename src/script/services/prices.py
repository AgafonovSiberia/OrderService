from datetime import datetime, date

from src.script.tools.google_api import get_worksheet
from pydantic import BaseModel, Field, validator

WORKSHEET_ID = 0


class Record(BaseModel):
    id: int = Field(alias="№")
    number: int = Field(alias="заказ №")
    price_by_dollar: int = Field(alias="стоимость,$")
    delivery_date: date = Field(alias="срок поставки")

    @validator("delivery_date", pre=True)
    def parse_date(cls, value):
        return datetime.strptime(value, "%d.%m.%Y").date()


def get_records_from_sheets() -> list[list]:
    """
    Получает все записи из GoogleSheet
    :return: list[list]
    """
    ws = get_worksheet(WORKSHEET_ID)
    values_list = ws.get_all_records()
    for value_row in values_list:
        #print(value_row)
        print(Record(**value_row))



def update_price_to_database():
    pass


def price_to_rub():
    pass


def get_rate_ruble():
    pass



