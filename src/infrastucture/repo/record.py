from decimal import Decimal
from src.script.schemas import RecordSchema
from src.infrastucture.db.models import Record
from src.infrastucture.repo.base.base import BaseSQLAlchemyRepo


class RecordRepo(BaseSQLAlchemyRepo):
    def add_record(self, record: RecordSchema, rate: Decimal):
        record = self._session.merge(
            Record(
                order_number=record.order_number,
                price_in_dollars=record.price_in_dollars,
                price_in_rubles=record.price_in_dollars * rate,
                delivery_date=record.delivery_date,
            )
        )

        self._session.commit()
        return record
