import time

from src.script.services.records import update_record_to_database
from src.infrastucture.db.factory import create_pool
from sqlalchemy.orm.session import sessionmaker

GOOGLE_API_TIMEOUT = 2


def script_run():
    pool: sessionmaker = create_pool()

    while True:
        update_record_to_database(pool=pool)
        time.sleep(GOOGLE_API_TIMEOUT)


if __name__ == "__main__":
    script_run()
