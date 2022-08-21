from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api
from resources import *

from db import db


class DevApplicationConfiguration:
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{config('DB_USER')}:{config('DB_PASSWORD')}"
        f"@localhost:{config('DB_PORT')}/{config('DATABASE')}"
    )


class TestApplicationConfiguration:
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{config('DB_USER')}:{config('DB_PASSWORD')}"
        f"@localhost:{config('DB_PORT')}/{config('TEST_DATABASE')}"
    )


def create_app(config = "config.DevApplicationConfiguration"):
    app = Flask(__name__)
    app.config.from_object(config)
    migrate = Migrate(app, db)
    CORS(app)
    api = Api(app)
    [api.add_resource(*r) for r in routes]
    return app