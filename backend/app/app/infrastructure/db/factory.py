from app.config_reader import config

from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import Engine
from sqlalchemy import create_engine


def create_pool():
    engine = create_engine(config.POSTGRES_URL, pool_pre_ping=True, echo=False)
    return create_session_maker(engine)


def create_session_maker(engine: Engine) -> sessionmaker:
    pool: sessionmaker = sessionmaker(engine, expire_on_commit=False, autoflush=False)
    return pool
