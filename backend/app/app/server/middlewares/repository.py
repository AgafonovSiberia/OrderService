from app.infrastructure.repo.base.repository import SQLALchemyRepo
from flask import Flask
from sqlalchemy.orm import sessionmaker


class RepositoryMiddleware:
    """Пробрасывает пул инстанст SQLALchemyRepo к хендлерам"""

    def __init__(self, app: Flask, pool: sessionmaker) -> None:
        self.app = app
        self.pool = pool

    def __call__(self, environ, start_response):
        with self.pool() as _session:
            environ["repo"] = SQLALchemyRepo(_session)
            return self.app(environ, start_response)
