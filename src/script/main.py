import time

from src.script.services.records import update_record_to_database
from src.infrastucture.db.factory import create_pool
from sqlalchemy.orm.session import sessionmaker


def start_script(sessions_pool: sessionmaker):
    while True:
        update_record_to_database(pool=sessions_pool)
        time.sleep(1.1)


if __name__ == "__main__":
    pool = create_pool()
    start_script(sessions_pool=pool)
