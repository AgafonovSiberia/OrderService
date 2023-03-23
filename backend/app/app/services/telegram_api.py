import requests

from app.config_reader import config
from requests import request

BASE_URL = "https://api.telegram.org/"


def send_message(text: str, chat_id: int):
    url = f"{BASE_URL}bot{config.BOT_TOKEN}/SendMessage"
    payload = {"chat_id": chat_id,
               "text": text,
               "parse_mode": "HTML",
               "chat_type": "private"}
    
    response = requests.post(url=url, data=payload)

