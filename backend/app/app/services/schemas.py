import datetime
from decimal import Decimal

from pydantic import BaseModel
from pydantic import Field
from pydantic import validator


class OrderSchema(BaseModel):
    order_number: int = Field(alias="заказ №")
    price_in_dollars: Decimal = Field(alias="стоимость,$")
    price_in_rubles: Decimal = Field(default=0)
    delivery_date: datetime.date = Field(alias="срок поставки")

    @validator("delivery_date", pre=True)
    def parse_date(cls, value):
        return datetime.datetime.strptime(value, "%d.%m.%Y").date()


# class OrderFullSchema(OrderSchema):
#
#
#     @validator("price_in_rubles", pre=True)
#     def convert_valute(cls, value):
#         return value * get_current_rate_from_api()
#
#     class Config:
#         orm_mode = True
