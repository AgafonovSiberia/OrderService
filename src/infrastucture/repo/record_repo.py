from decimal import Decimal
from sqlalchemy.dialects.postgresql import insert

from src.script.schemas import RecordSchema
from src.infrastucture.db.models import Record
from src.infrastucture.repo.base.base import BaseSQLAlchemyRepo


class RecordRepo(BaseSQLAlchemyRepo):
    def add_record(self, new_record: RecordSchema, rate: Decimal):
        new_record = Record(
            order_number=new_record.order_number,
            price_in_dollars=new_record.price_in_dollars,
            price_in_rubles=new_record.price_in_dollars * rate,
            delivery_date=new_record.delivery_date,
        )

        record: Record = self._session.execute(
            insert(Record)
            .values(
                order_number=new_record.order_number,
                price_in_dollars=new_record.price_in_dollars,
                price_in_rubles=new_record.price_in_rubles,
                delivery_date=new_record.delivery_date,
            )
            .on_conflict_do_update(
                index_elements=["order_number"],
                set_={
                    "price_in_dollars": new_record.price_in_dollars,
                    "price_in_rubles": new_record.price_in_rubles,
                    "delivery_date": new_record.delivery_date,
                },
            )
            .returning(Record)
        )

        self._session.commit()
        return record

    # upset multi rows
    def add_records(self, records_list: list[RecordSchema], rate: Decimal):
        prepare_data = [
            dict(
                order_number=record.order_number,
                price_in_dollars=record.price_in_dollars,
                price_in_rubles=record.price_in_dollars * rate,
                delivery_date=record.delivery_date,
            )
            for record in records_list
        ]

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
