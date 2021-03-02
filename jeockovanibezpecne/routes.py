from datetime import datetime

import click
from flask import render_template, send_from_directory, request
from flask import current_app as app
from flask.cli import with_appcontext

from .models import Submit, Vaccine, Dead, Case

from .database import init_db_command
from .update import update


@click.command("update")
@with_appcontext
def update_command():
    update()
    click.echo("Database updated.")


def init_app(app):
    app.cli.add_command(init_db_command)
    app.cli.add_command(update_command)


@app.route("/", methods=["GET"])
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
    return "{0:,}".format(value).replace(",", "&thinsp;")


@app.template_filter()
def fmt_date(value):
    return datetime.strftime(value, "%m. %d. %Y").lstrip("0").replace(" 0", " ")


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
