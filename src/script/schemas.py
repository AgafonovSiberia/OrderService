from datetime import datetime, date
from pydantic import BaseModel, Field, validator
from decimal import Decimal
from src.script.services.current_rate import get_current_rate_from_api


class RecordSchema(BaseModel):
    order_number: int = Field(alias="заказ №")
    price_in_dollars: Decimal = Field(alias="стоимость,$")
    delivery_date: date = Field(alias="срок поставки")

    @validator("delivery_date", pre=True)
    def parse_date(cls, value):
        return datetime.strptime(value, "%d.%m.%Y").date()


class RecordFullSchema(RecordSchema):
    price_in_rubles: Decimal = Field(alias="стоимость,$")

    @validator("price_in_rubles", pre=True)
    def convert_valute(cls, value):
        return value * get_current_rate_from_api()

    class Config:
        orm_mode = True
