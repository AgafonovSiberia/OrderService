import datetime

import requests
from decimal import Decimal
from xml.etree.ElementTree import fromstring
from functools import lru_cache
from src.logger import logger

USD_CODE = "R01235"
URL_API = "https://www.cbr.ru/scripts/XML_daily.asp"


@lru_cache(maxsize=3)
def get_current_rate_from_api(
    date: datetime.date = datetime.date.today(),
) -> Decimal | None:
    """
    Получает актуальный курс USD через API ЦБ РФ
    :return: Decimal | None
    """
    url = f"{URL_API}?date_req={date.strftime('%d/%m/%Y')}"

    result = requests.get(url)
    if result.status_code == 200:
        root = fromstring(result.text).find(f"Valute[@ID='{USD_CODE}']")
        rate = root.find("Value")

        logger.info(f"От ЦБ РФ получен курс валют на {date}. Курс USD-RUB: {rate.text}")
        return convert_rate_to_decimal(rate=rate)

    logger.error(
        f"Не удалось получить актуальный курс валют от ЦБ РФ на {date}. {result.status_code}"
    )
    return get_current_rate_from_api.__wrapped__()


def convert_rate_to_decimal(rate: str):
    """
    Переводит курс доллара из str в Decimal в виде строки
    :param rate: курс доллара, полученный от API (77,12) в виде строки с ,
    :return: Decimal('77.12')
    """
    rate_decimal = Decimal(rate.text.replace(",", ".", 1))
    return rate_decimal
