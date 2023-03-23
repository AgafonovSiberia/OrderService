from flask import Flask
from app.infrastucture.db.factory import create_pool
from app.server.middlewares.repository import Repository
from app.server.routes import router


def setup_blueprints():
    app.register_blueprint(router)


def create_app() -> Flask:
    flask_app = Flask(__name__)
    return flask_app


if __name__ == "__main__":
    print("Я жив")
    app = create_app()
    setup_blueprints()
    pool = create_pool()
    app.wsgi_app = Repository(app.wsgi_app, pool)
    app.run(host='0.0.0.0', port=9090)

