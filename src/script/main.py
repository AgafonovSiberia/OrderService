import time
from src.script.services.core import update_orders_to_database
from src.infrastucture.db.factory import create_pool
from sqlalchemy.orm.session import sessionmaker
from src.logger import logger

# Quota limits to GoogleSheets APi. Per minute per user per project - 60
GOOGLE_API_TIMEOUT = 2


def script_run():
    logger.info("Script started")
    pool: sessionmaker = create_pool()

    while True:
        update_orders_to_database(pool=pool)
        time.sleep(GOOGLE_API_TIMEOUT)


if __name__ == "__main__":
    #script_run()
    while True:
        print("hello")
