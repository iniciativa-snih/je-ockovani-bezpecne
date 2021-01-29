from flask import request, render_template, make_response
from datetime import datetime as dt
from flask import current_app as app

from .models import db, Stat


@app.route('/', methods=['GET'])
def index():
    stats = Stat.query.all()
    return render_template('stats/stats.jinja2', stats=stats)
