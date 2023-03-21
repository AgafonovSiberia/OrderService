import requests
from xml.etree.ElementTree import fromstring

USD_CODE = "R01235"
URL_API = "https://www.cbr.ru/scripts/XML_daily.asp"


def get_current_rate(val_id: str) -> float:
    result = requests.get(URL_API)
    root = fromstring(result.text).find(f"Valute[@ID={val_id}]")
    rate = root.find("Value")
    return float(rate.text.replace(",", ".", 1))




