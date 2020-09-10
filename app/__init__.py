import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config

db = SQLAlchemy()


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(Config)
    os.makedirs(app.static_folder, exist_ok=True)

    db.init_app(app)

    from .api import bp
    app.register_blueprint(bp, url_prefix="/api/v1/")

    return app
