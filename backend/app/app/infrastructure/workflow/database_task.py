from abc import ABC

from app.infrastructure.db.factory import create_pool
from app.infrastructure.repo.base.repository import SQLALchemyRepo
from celery import Task


class DatabaseTask(Task, ABC):
    _session = None

    def after_return(self, *args, **kwargs):
        if self._session is not None:
            self._session.close()

    @property
    def repo(self):
        if self._session is None:
            pool = create_pool()
            self._session = pool()
        return SQLALchemyRepo(self._session)
