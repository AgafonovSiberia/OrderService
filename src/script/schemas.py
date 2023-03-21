from datetime import datetime, date
from pydantic import BaseModel, Field, validator
from decimal import Decimal


class RecordSchema(BaseModel):
    id: int = Field(alias="№")
    order_number: int = Field(alias="заказ №")
    price_in_dollars: Decimal = Field(alias="стоимость,$")
    delivery_date: date = Field(alias="срок поставки")

    @validator("delivery_date", pre=True)
    def parse_date(cls, value):
        return datetime.strptime(value, "%d.%m.%Y").date()
