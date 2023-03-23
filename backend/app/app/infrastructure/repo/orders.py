from sqlalchemy.dialects.postgresql import insert

from app.services.schemas import OrderFullSchema
from app.infrastructure.db.models import Order
from app.infrastructure.repo.base.base import BaseSQLAlchemyRepo
import datetime
from sqlalchemy import select, func
from decimal import Decimal
from app.config_reader import config
from pytz import timezone

class OrderRepo(BaseSQLAlchemyRepo):
    # upsert multi rows
    def add_orders(self, orders_list: list[OrderFullSchema]):
        prepare_data = [record.dict() for record in orders_list]
        ins = insert(Order).values(prepare_data)

        query = ins.on_conflict_do_update(
            index_elements=["order_number"],
            set_={
                "price_in_dollars": ins.excluded.price_in_dollars,
                "price_in_rubles": ins.excluded.price_in_rubles,
                "delivery_date": ins.excluded.delivery_date,
            },
        )

        self._session.execute(query)
        self._session.commit()

    def get_orders(self):
        orders = self._session.execute(select(Order))
        self._session.commit()
        return orders.scalars().all()

    def get_total_sum_in_dollars(self) -> Decimal:
        totals = self._session.execute(select(func.sum(Order.price_in_dollars),
                                              func.sum(Order.price_in_rubles)))
        return totals.first()

    def get_prices_in_dollars_dynamic(self):
        prices_list = self._session.execute(select(Order.price_in_dollars))
        return prices_list.scalars().all()

    def get_expire_orders(self, zone: str = config.TIMEZONE):
        now = datetime.datetime.now(timezone(zone))
        today = datetime.date(now.year, now.month, now.day)

        expire_orders_list = self._session.execute(
            select(Order).
            where(Order.delivery_date == today)
        )
        return expire_orders_list.scalars().all()


