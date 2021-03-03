from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, ".env"))


class Config(object):
    DEBUG = True
    TESTING = True
    DEVELOPMENT = True

    CSRF_ENABLED = True
    SECRET_KEY = "this-really-needs-to-be-changed"
    SQLALCHEMY_DATABASE_URI = environ["DATABASE_URL"]


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    DEVELOPMENT = False


class DevelopmentConfig(Config):
    TESTING = False


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite://"
