import time

from src.script.services.core import update_record_to_database
from src.infrastucture.db.factory import create_pool
from sqlalchemy.orm.session import sessionmaker
from src.script.services.google_api import get_worksheet
from src.logger import logger

GOOGLE_API_TIMEOUT = 2


def script_run():
    logger.info("Start script")
    pool: sessionmaker = create_pool()
    ws = get_worksheet(0)

    while True:
        update_record_to_database(pool=pool, ws=ws)
        time.sleep(GOOGLE_API_TIMEOUT)


if __name__ == "__main__":
    script_run()
