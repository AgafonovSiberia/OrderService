from decimal import Decimal
from sqlalchemy.dialects.postgresql import insert

from src.script.schemas import OrderFullSchema
from src.infrastucture.db.models import Orders
from src.infrastucture.repo.base.base import BaseSQLAlchemyRepo


class OrderRepo(BaseSQLAlchemyRepo):
    # upsert multi rows
    def add_orders(self, orders_list: list[OrderFullSchema]):
        prepare_data = [record.dict() for record in orders_list]
        ins = insert(Orders).values(prepare_data)

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
