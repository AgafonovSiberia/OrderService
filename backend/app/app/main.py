from app.infrastructure.db.factory import create_pool
from app.logger import logger
from app.server.middlewares.repository import RepositoryMiddleware
from app.server.routes import router
from flask import Flask
from flask_cors import CORS


def setup_blueprints() -> None:
    """
    Регистрирует роутеры
    """
    app.register_blueprint(router)


def create_app() -> Flask:
    flask_app = Flask(__name__)
    CORS(flask_app)

    pool = create_pool()
    flask_app.wsgi_app = RepositoryMiddleware(flask_app.wsgi_app, pool)
    return flask_app


if __name__ == "__main__":
    app = create_app()
    setup_blueprints()
    logger.info("Starting server")
    app.run(host="0.0.0.0", port=9090)
