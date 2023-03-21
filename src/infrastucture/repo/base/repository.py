from sqlalchemy.ext.asyncio import AsyncSession
from functools import lru_cache
from typing import Type, TypeVar

from src.infrastucture.repo.base.base import BaseSQLAlchemyRepo


T = TypeVar("T", bound=BaseSQLAlchemyRepo)


class SQLALchemyRepo:
    def __init__(self, session: AsyncSession):
        self._session = session

    @lru_cache()
    def get_repo(self, repo: Type[T]) -> T:
        return repo(self._session)

    def commit(self):
        self._session.commit()

    def rollback(self):
        self._session.rollback()
