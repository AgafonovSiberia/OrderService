from decimal import Decimal
from sqlalchemy.dialects.postgresql import insert

from src.script.schemas import RecordFullSchema
from src.infrastucture.db.models import Record
from src.infrastucture.repo.base.base import BaseSQLAlchemyRepo


class RecordRepo(BaseSQLAlchemyRepo):
    # upsert multi rows
    def add_records(self, records_list: list[RecordFullSchema], rate: Decimal):
        prepare_data = [record.dict() for record in records_list]
        ins = insert(Record).values(prepare_data)

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
