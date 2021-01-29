import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

db = SQLAlchemy()

def create_app(test_config=None):
    # create and configure the app
    # app = Flask(__name__, instance_relative_config=True)

    app = Flask(__name__, instance_relative_config=False)

    config_class = os.environ['APP_SETTINGS'] if test_config is None else test_config
    app.config.from_object(config_class)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
 
    db.init_app(app)
    migrate = Migrate(app, db)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    with app.app_context():
        from . import routes

        return app
