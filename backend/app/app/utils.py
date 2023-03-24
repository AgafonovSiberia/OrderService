import datetime
import time
from typing import Callable

from app.config_reader import config
from app.logger import logger
from pytz import timezone


def timeit(func: Callable) -> Callable:
    """
    Декоратор вычисление времени выполнения функции
    :param func: декорируемая функция
    """

    def wrapper(*args, **kwargs):
        start_time = time.monotonic()
        result = func(*args, **kwargs)
        end_time = time.monotonic()
        logger.info(
            f"{func.__name__} - duration: {datetime.timedelta(seconds=end_time - start_time)}"
        )
        return result

    return wrapper


def get_today_with_timezone():
    """
    Получает текущую дату с учётом часового пояса,
    определённого в config.TIMEZONE
    :return: сегодняшняя дата с учётом часового пояса
    """
    now = datetime.datetime.now(timezone(config.TIMEZONE))
    today = datetime.date(now.year, now.month, now.day)
    return today
