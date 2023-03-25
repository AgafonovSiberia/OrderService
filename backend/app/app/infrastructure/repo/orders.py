from decimal import Decimal

from app.infrastructure.db.models import Order
from app.infrastructure.repo.base.base import BaseSQLAlchemyRepo
from app.services.schemas import OrderSchema
from app.utils import get_today_with_timezone
from sqlalchemy import desc
from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert


class OrderRepo(BaseSQLAlchemyRepo):
    """
    Имплементация паттерна Repository для модели Order
    """

    def add_orders(self, orders_list: list[OrderSchema]) -> None:
        """
        Добавляет/обновляет (upsert) все заказыв БД
        :param orders_list: список с pydantic моделями OrderShema
        """
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

    def get_orders(self) -> list[Order]:
        """
        Достаёт из БД все заказы
        :return: список с моделями алхимии - Order
        """
        orders = self._session.execute(select(Order))
        return orders.scalars().all()

    def get_total_sum(self) -> tuple[Decimal, Decimal]:
        """
        Достаёт из базы данных сумму всех текущих заказов в долларах и рублях
        :return: кортеж (сумма в долларах, сумма в рублях)
        """
        totals = self._session.execute(
            select(func.sum(Order.price_in_dollars), func.sum(Order.price_in_rubles))
        )
        return totals.first()

    def get_prices_in_dollars_dynamic(self) -> list[Decimal]:
        """
        Достаёт из БД стоимости заказов в долларах,
        отсортированные по дате
        :return: список стоимостей в долларах
        """
        prices_list = self._session.execute(select(Order).order_by(desc(Order.delivery_date)))
        prices_list = prices_list.scalars().all()

        return [
            {"date": order.delivery_date.strftime("%d.%m.%Y"), "price": int(order.price_in_dollars)}
            for order in prices_list
        ]

    def get_expire_orders(self) -> list[Order]:
        """
        Достаёт из БД список всех заказов, которые истекают сегодня
        :return: список с моделями алхимии - Order
        """
        today = get_today_with_timezone()

        expire_orders_list = self._session.execute(
            select(Order).where(Order.delivery_date == today)
        )
        return expire_orders_list.scalars().all()
