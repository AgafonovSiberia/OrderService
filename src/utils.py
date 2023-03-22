from src.logger import logger
import time
from datetime import timedelta


def timeit(func):
    def wrapper(*args, **kwargs):
        start_time = time.monotonic()
        result = func(*args, **kwargs)
        end_time = time.monotonic()
        logger.info(
            f"{func.__name__} - duration: {timedelta(seconds=end_time - start_time)}"
        )
        return result

    return wrapper
