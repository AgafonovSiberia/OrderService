from flask import Blueprint, request, Response, jsonify
from app.infrastructure.repo.base.repository import SQLALchemyRepo
from app.infrastructure.repo.orders import OrderRepo
from app.infrastructure.db.models import Order
from decimal import Decimal

router = Blueprint('simple_page', __name__)


@router.get("/orders")
def get_orders_list():
    repo: SQLALchemyRepo = request.environ['repo']
    orders_list: list[Order] = repo.get_repo(OrderRepo).get_orders()
    return jsonify([order.to_dict for order in orders_list])


@router.get("/total")
def get_total_in_dollars():
    repo: SQLALchemyRepo = request.environ['repo']
    total_in_dollars, total_in_rubles = repo.get_repo(OrderRepo).get_total_sum_in_dollars()
    return jsonify({"total_sum_in_dollars": total_in_dollars, "total_sum_in_rubles": total_in_rubles})


@router.get("/price_dynamic")
def get_price_dynamic():
    repo: SQLALchemyRepo = request.environ['repo']
    prices_dynamic = repo.get_repo(OrderRepo).get_prices_in_dollars_dynamic()
    print(prices_dynamic)
    return prices_dynamic


@router.get("/check_expire_orders")
def check_expire_orders():
    repo: SQLALchemyRepo = request.environ['repo']
    expire_orders_list = repo.get_repo(OrderRepo).get_expire_orders()
    data = [order.to_dict for order in expire_orders_list]
    print(data)
    return jsonify(data)
