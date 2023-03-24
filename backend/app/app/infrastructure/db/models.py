from app.infrastructure.db.base import Base
from sqlalchemy import BigInteger
from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import DECIMAL
from sqlalchemy import Integer


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    order_number = Column(BigInteger, nullable=False, unique=True)
    price_in_dollars = Column(DECIMAL(asdecimal=True), nullable=False)
    price_in_rubles = Column(DECIMAL(asdecimal=True), nullable=False)
    delivery_date = Column(Date, default=None, index=True)

    @property
    def to_dict(self):
        return {
            "id": self.id,
            "order_number": self.order_number,
            "price_in_dollars": self.price_in_dollars,
            "price_in_rubles": self.price_in_rubles,
            "delivery_date": self.delivery_date.strftime("%d.%m.%Y"),
        }
