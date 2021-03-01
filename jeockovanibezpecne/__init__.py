import os

from flask import Flask

# from flask_migrate import Migrate
from flask_babel import Babel


def create_app(test_config=None):
    # create and configure the app
    # app = Flask(__name__, instance_relative_config=True)

    app = Flask(__name__, instance_relative_config=False, static_folder="static")

    config_class = os.environ["APP_SETTINGS"] if test_config is None else test_config
    app.config.from_object(config_class)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # migrate = Migrate(app, db)

    babel = Babel(app)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    with app.app_context():
        from . import routes

        from .routes import init_app

        init_app(app)

        return app
