from decimal import Decimal
from sqlalchemy.dialects.postgresql import insert

from src.script.schemas import RecordSchema
from src.infrastucture.db.models import Record
from src.infrastucture.repo.base.base import BaseSQLAlchemyRepo


class RecordRepo(BaseSQLAlchemyRepo):
    def add_record(self, record: RecordSchema, rate: Decimal):
        record = Record(
            order_number=record.order_number,
            price_in_dollars=record.price_in_dollars,
            price_in_rubles=record.price_in_dollars * rate,
            delivery_date=record.delivery_date,
        )

        record = self._session.execute(
            insert(Record)
            .values(
                order_number=record.order_number,
                price_in_dollars=record.price_in_dollars,
                price_in_rubles=record.price_in_rubles,
                delivery_date=record.delivery_date,
            )
            .on_conflict_do_update(
                index_elements=["order_number"],
                set_={
                    "price_in_dollars": record.price_in_dollars,
                    "price_in_rubles": record.price_in_rubles,
                    "delivery_date": record.delivery_date,
                },
            )
            .returning(Record)
        )

        self._session.commit()
        return record
