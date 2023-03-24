import requests
from app.config_reader import config
from app.logger import logger
from app.templates.order_expire import ORDER_EXPIRE_HEADER

BASE_URL = "https://api.telegram.org/"


def emailing_to_admins(message: str):
    for chat_id in config.ID_ADMINS:
        send_message(message, chat_id)


def send_message(text: str, chat_id: int):
    url = f"{BASE_URL}bot{config.BOT_TOKEN}/SendMessage"
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "HTML", "chat_type": "private"}

    response = requests.post(url=url, data=payload)
    if response.status_code != 200:
        logger.log(f"Не удалось доставить сообщение. chat_id: {chat_id}")


def render_message_order_expire(data: list[dict]):
    orders_info = ""
    for idx, order in enumerate(data, start=1):
        orders_info += (
            f"<b>{idx}</b>.Номер заказа: <i>{order.order_number}</i>\n"
            f"Стоимость(USD/RUB): <i> {order.price_in_dollars} "
            f"/ {order.price_in_rubles}</i>\n\n"
        )
    message = f"{ORDER_EXPIRE_HEADER}{orders_info}"
    return message
