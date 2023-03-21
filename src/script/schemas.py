
from datetime import datetime, date
from pydantic import BaseModel, Field, validator

class Record(BaseModel):
    id: int = Field(alias="№")
    number: int = Field(alias="заказ №")
    price_by_dollar: int = Field(alias="стоимость,$")
    delivery_date: date = Field(alias="срок поставки")

    @validator("delivery_date", pre=True)
    def parse_date(cls, value):
        return datetime.strptime(value, "%d.%m.%Y").date()
