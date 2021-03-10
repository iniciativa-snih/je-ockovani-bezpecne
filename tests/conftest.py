import pytest
from datetime import datetime

from jeockovanibezpecne import create_app


@pytest.fixture
def app():
    app = create_app("config.TestingConfig")

    with app.app_context():
        from jeockovanibezpecne.init import fmt_date, fmt_number

        app.jinja_env.filters["fmt_date"] = fmt_date
        app.jinja_env.filters["fmt_number"] = fmt_number

        from jeockovanibezpecne.database import init_db, db_session
        from jeockovanibezpecne.models import Dead, Vaccine, Submit, Case

        init_db()

        db_session.connection().execute("DELETE FROM submits")
        db_session.add(Submit(datetime.now(), datetime(2021, 3, 10), 100))
        db_session.add(Submit(datetime.now(), datetime(2021, 3, 9), 150))

        db_session.connection().execute("DELETE FROM vaccines")
        db_session.add(Vaccine(datetime.now(), datetime(2021, 3, 10), 200, 50))
        db_session.add(Vaccine(datetime.now(), datetime(2021, 3, 9), 150, 30))
        db_session.add(Vaccine(datetime.now(), datetime(2021, 3, 8), 100, 20))

        db_session.connection().execute("DELETE FROM deads")
        db_session.add(Dead(datetime.now(), datetime(2021, 3, 10), 200))
        db_session.add(Dead(datetime.now(), datetime(2021, 3, 9), 150))
        db_session.add(Dead(datetime.now(), datetime(2021, 3, 8), 100))

        db_session.connection().execute("DELETE FROM cases")
        db_session.add(Case(datetime.now(), datetime(2021, 3, 10), 20, 180))
        db_session.add(Case(datetime.now(), datetime(2021, 3, 9), 50, 160))
        db_session.add(Case(datetime.now(), datetime(2021, 3, 8), 100, 110))
        db_session.add(Case(datetime.now(), datetime(2021, 3, 7), 10, 10))

        db_session.commit()

    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
