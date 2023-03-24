from app.config_reader import config
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker


def create_pool() -> sessionmaker:
    """
    Создаёт SQLAlchemy Engine и возвращает пул подключений
    """
    engine = create_engine(config.POSTGRES_URL, pool_pre_ping=True, echo=False)
    return create_session_maker(engine)


def create_session_maker(engine: Engine) -> sessionmaker:
    """Создаёт пул подключений к БД"""
    pool: sessionmaker = sessionmaker(engine, expire_on_commit=False, autoflush=False)
    return pool
