import click
from flask import current_app as app
from flask.cli import with_appcontext
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    from .models import Submit, Vaccine, Dead, Case  # noqa: F401

    Base.metadata.create_all(bind=engine)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@contextmanager
def transaction():
    try:
        yield
        db_session.commit()
    except Exception:
        db_session.rollback()
        raise


@click.command("init-db")
@with_appcontext
def init_db_command():
    init_db()
    click.echo("Initialized the database.")
