from app.config_reader import config
from app.infrastructure.db.models import Order
from app.infrastructure.repo.base.repository import SQLALchemyRepo
from app.infrastructure.repo.orders import OrderRepo
from app.infrastructure.workflow.tasks.check_delivery_task import check_delivery_expire_task
from flask import Blueprint
from flask import jsonify
from flask import request
from flask import Response

router = Blueprint("api", __name__, url_prefix=config.API_V1_URL)


@router.get("/orders")
def get_orders_list() -> Response:
    """
    Отдаёт все заказы из БД
    """
    repo: SQLALchemyRepo = request.environ["repo"]
    orders_list: list[Order] = repo.get_repo(OrderRepo).get_orders()
    return jsonify([order.to_dict for order in orders_list])


@router.get("/total")
def get_total_in_dollars() -> Response:
    """
    Отдаёт суммы всех текущих заказов в долларах и рублях
    """
    repo: SQLALchemyRepo = request.environ["repo"]
    total_in_dollars, total_in_rubles = repo.get_repo(OrderRepo).get_total_sum()
    return jsonify(
        [{"total_sum_in_dollars": total_in_dollars, "total_sum_in_rubles": total_in_rubles}]
    )


@router.get("/price_dynamic")
def get_price_dynamic() -> Response:
    """
    Отдаёт стоимости всех заказов в $, отскорированные по дате
    """
    repo: SQLALchemyRepo = request.environ["repo"]
    prices_dynamic = repo.get_repo(OrderRepo).get_prices_in_dollars_dynamic()

    return prices_dynamic


@router.get("/check_expire_orders")
def check_expire_orders() -> Response:
    """
    Принудительно вызывает таску проверки истекающих заказов.
    Если такие заказы есть, будет отправлено
    сообщение в Telegram (для config.ID_ADMINS)
    """
    check_delivery_expire_task.delay()
    resp = jsonify(success=True)
    resp.status_code = 200
    return resp
