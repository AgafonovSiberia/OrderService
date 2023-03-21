from sqlalchemy import Column, Integer, Date, DECIMAL
from src.infrastucture.db.base import Base


class Record(Base):
    __tablename__ = "records"
    id = Column(Integer, primary_key=True)
    order_number = Column(Integer, nullable=False, unique=True)
    price_in_dollars = Column(DECIMAL(asdecimal=True), nullable=False)
    price_in_rubles = Column(DECIMAL(asdecimal=True), nullable=False)
    delivery_date = Column(Date, default=None, index=True)
