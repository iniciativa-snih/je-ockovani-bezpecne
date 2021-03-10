from flask import Blueprint
from datetime import datetime

from flask import render_template, send_from_directory, request
from flask import current_app as app

from .models import Vaccine, Dead, Case


bp = Blueprint("stats", __name__)


@bp.route("/hello")
def hello():
    return "Hello, world"


@bp.route("/", methods=["GET"])
def index():
    date_from = datetime(2020, 12, 27)

    cases = Case.query.order_by(Case.date_for.desc()).all()
    date_for = cases[0].date_for

    cases_for = Case.query.order_by(Case.date_for.desc()).first()
    cases_no = cases_for.cases_cumulative

    vaccines = Vaccine.query.filter(Vaccine.date_for >= date_from).filter(Vaccine.date_for <= date_for).all()
    vaccinated_no = sum([v.first_vaccines for v in vaccines])

    deads_for = Dead.query.order_by(Dead.date_for.desc()).first()
    deads_no = deads_for.deads_cumulative

    return render_template(
        "index.jinja2",
        vaccinated=vaccinated_no,
        deads=deads_no,
        date_from=date_from,
        date_for=date_for,
        cases=cases_no,
    )


@bp.route("/favicon.ico")
def favicon():
    return send_from_directory(app.static_folder, "favicon.ico", mimetype="image/vnd.microsoft.icon")


@app.route("/robots.txt")
@app.route("/humans.txt")
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])


@bp.errorhandler(404)
def page_not_found(e):
    return render_template("404.jinja2"), 404
