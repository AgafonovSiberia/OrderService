from src.config_reader import config


from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
    AsyncEngine,
)


def create_pool() -> async_sessionmaker[AsyncSession]:
    engine = create_async_engine(config.POSTGRES_URL, pool_pre_ping=True, echo=True)
    return create_session_maker(engine)


def create_session_maker(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    pool: async_sessionmaker[AsyncSession] = async_sessionmaker(
        bind=engine, expire_on_commit=False, autoflush=False
    )
    return pool
