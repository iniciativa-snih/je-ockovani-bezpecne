import os

from flask import Flask
from flask_babel import Babel


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=False, static_folder="static")

    config_class = os.environ["APP_SETTINGS"] if test_config is None else test_config
    app.config.from_object(config_class)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # migrate = Migrate(app, db)

    babel = Babel(app)

    with app.app_context():
        from . import init

        from .init import init_app

        init_app(app)

        from . import stats

        app.register_blueprint(stats.bp)

        return app
