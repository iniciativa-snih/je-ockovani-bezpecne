import click
from flask import render_template
from datetime import timedelta
from flask import current_app as app
from flask.cli import with_appcontext
from contextlib import contextmanager

from .models import Submit, Vaccine, Dead, Case

from .database import db, init_db


@app.teardown_appcontext
def shutdown_session(exception=None):
    db.remove()


@contextmanager
def transaction():
    try:
        yield
        db.commit()
    except Exception:
        db.rollback()
        raise


@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.cli.add_command(init_db_command)


@app.route('/', methods=['GET'])
@transaction()
def index():
    submit = Submit.query.order_by(Submit.date_for.desc()).limit(2).all()
    date_for = submit[0].date_for
    date_from = date_for - timedelta(days=6)
    submits_no = submit[0].submits - submit[1].submits

    vaccines = (Vaccine.query
        .filter(Vaccine.date_for >= date_from)
        .filter(Vaccine.date_for <= date_for)
        .all()
    )
    vaccines_no = sum([v.first_vaccines + v.second_vaccines for v in vaccines])

    deads_from = Dead.query.filter(Dead.date_for == date_from).first()
    deads_for = Dead.query.filter(Dead.date_for == date_for).first()
    deads_no = deads_for.deads_cumulative - deads_from.deads_cumulative

    cases_from = Case.query.filter(Case.date_for == date_from).first()
    cases_for = Case.query.filter(Case.date_for == date_for).first()
    cases_no = cases_for.cases_cumulative - cases_from.cases_cumulative

    cases = Case.query.order_by(Case.date_for.desc()).first()

    return render_template('stats/stats.jinja2', submit=submit, submits=submits_no,
                           vaccines=vaccines_no, deads=deads_no,
                           date_from=date_from, date_for=date_for,
                           cases=cases_no, date_covid_update=cases.date_for)


@app.route('/hello', methods=['GET'])
def hello():
    return render_template('index.jinja2')
