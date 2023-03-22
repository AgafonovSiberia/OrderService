import requests
from decimal import Decimal
from xml.etree.ElementTree import fromstring

USD_CODE = "R01235"
URL_API = "https://www.cbr.ru/scripts/XML_daily.asp"


def get_current_rate_from_api() -> Decimal | None:
    """
    Получает актуальный курс USD через API ЦБ РФ
    :return: Decimal | None
    """
    result = requests.get(URL_API)
    if result.status_code == 200:
        root = fromstring(result.text).find(f"Valute[@ID='{USD_CODE}']")
        rate = root.find("Value")
        return convert_rate_to_decimal(rate=rate)
    # add record to logger
    return None


def convert_rate_to_decimal(rate: str):
    """
    Переводит курс доллара из str в Decimal в виде строки
    :param rate: курс доллара, полученный от API (77,12) в виде строки с ,
    :return: Decimal('77.12')
    """
    rate_decimal = Decimal(rate.text.replace(",", ".", 1))
    return rate_decimal
