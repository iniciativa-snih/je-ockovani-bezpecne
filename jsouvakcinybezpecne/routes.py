import click
from flask import render_template, send_from_directory, request
from datetime import datetime
from flask import current_app as app
from flask.cli import with_appcontext
from contextlib import contextmanager
from flask_babel import format_date

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


@click.command("init-db")
@with_appcontext
def init_db_command():
    init_db()
    click.echo("Initialized the database.")


def init_app(app):
    app.cli.add_command(init_db_command)


@app.route("/", methods=["GET"])
@transaction()
def index():
    submit = Submit.query.order_by(Submit.date_for.desc()).first()
    date_for = submit.date_for
    date_from = datetime(2020, 12, 27)

    vaccines = Vaccine.query.filter(Vaccine.date_for >= date_from).filter(Vaccine.date_for <= date_for).all()
    vaccinated_no = sum([v.first_vaccines for v in vaccines])

    deads_from = Dead.query.filter(Dead.date_for == date_from).first()
    deads_for = Dead.query.filter(Dead.date_for == date_for).first()
    deads_no = deads_for.deads_cumulative - deads_from.deads_cumulative

    cases_from = Case.query.filter(Case.date_for == date_from).first()
    cases_for = Case.query.filter(Case.date_for == date_for).first()
    cases_no = cases_for.cases_cumulative - cases_from.cases_cumulative

    return render_template(
        "index.jinja2",
        submit=submit,
        vaccinated=vaccinated_no,
        deads=deads_no,
        date_from=date_from,
        date_for=date_for,
        cases=cases_no,
    )


@app.template_filter()
def fmt_number(value):
    # https://stackoverflow.com/q/36889758/5763764
    return '{0:,}'.format(value).replace(',', '&thinsp;')


@app.template_filter()
def fmt_date(value):
    return format_date(value, locale='cs')


app.jinja_env.filters["fmt_number"] = fmt_number
app.jinja_env.filters["fmt_date"] = fmt_date


@app.route("/robots.txt")
@app.route("/humans.txt")
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(app.static_folder, "favicon.ico", mimetype="image/vnd.microsoft.icon")


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.jinja2"), 404
