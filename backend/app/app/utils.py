import datetime
import time

from app.config_reader import config
from app.logger import logger
from pytz import timezone


def timeit(func):
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
    now = datetime.datetime.now(timezone(config.TIMEZONE))
    today = datetime.date(now.year, now.month, now.day)
    print(type(today))
    return today
