from flask import Blueprint, request
from app.config_reader import config
from app.infrastucture.repo.base.repository import SQLALchemyRepo
from app.infrastucture.repo.orders import OrderRepo


router = Blueprint('simple_page', __name__)


@router.get("/orders")
def get_orders_list():
    repo: SQLALchemyRepo = request.environ['repo']
    result = repo.get_repo(OrderRepo).get_orders()
    return result


@router.get("/total_by_rubles")
def get_total_by_rubles():
    pass


@router.get("/price_dynamic")
def get_price_dynamic():
    pass


