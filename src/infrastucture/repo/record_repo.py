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

    # upser multi rows
    # def add_records(self, records_list: list[RecordSchema], rate: Decimal):
    #     ins = insert(Record).values(records_list)
    #
    #     exclude_for_update = [Record.id.name, "order_number", "price_in_rubles"]
    #
    #     update_dict = {c.name: c for c in ins.excluded if c.name not in exclude_for_update}
    #     print(f"Dict: {update_dict}")
    #
    #     query = ins.on_conflict_do_update(
    #         index_elements=["order_number"],
    #         set_=update_dict)
    #
    #     self._session.execute(query)
    #     self._session.commit()
