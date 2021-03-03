import os

from flask import Flask
from flask_babel import Babel


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=False, static_folder="static")

    if test_config is not None:
        config_class = test_config
    elif "APP_SETTINGS" in os.environ:
        config_class = os.environ["APP_SETTINGS"]
    else:
        print("APP_SETTINGS env var is missing config class, provide one")
        exit(1)
    app.config.from_object(config_class)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # migrate = Migrate(app, db)

    babel = Babel(app)  # noqa: F841

    with app.app_context():
        from . import init  # noqa: F401

        from .init import init_app

        init_app(app)

        from . import stats

        app.register_blueprint(stats.bp)

        return app
