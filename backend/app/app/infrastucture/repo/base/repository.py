from sqlalchemy.orm import Session
from functools import lru_cache
from typing import Type, TypeVar

from app.infrastucture.repo.base.base import BaseSQLAlchemyRepo


T = TypeVar("T", bound=BaseSQLAlchemyRepo)


def get_base_repo(session):
    return SQLALchemyRepo(session)


class SQLALchemyRepo:
    def __init__(self, session: Session):
        self._session = session

    @lru_cache()
    def get_repo(self, repo: Type[T]) -> T:
        return repo(self._session)

    def commit(self):
        self._session.commit()

    def rollback(self):
        self._session.rollback()
