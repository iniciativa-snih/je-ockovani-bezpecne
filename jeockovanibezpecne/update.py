import pandas as pd
from gazpacho import get, Soup
from datetime import datetime
from sqlalchemy import desc

from .models import Submit
from .database import db


def get_submits(timestamp):
    def parse_effect(tr):
        effect = tr.find("p")[0].text
        info = tr.find("p")[1].text
        span = tr.find("span")
        count = int(span.text if span is not None else tr.find("td")[1].find("p").text)
        return {"date_for": date_for, "effect": effect, "info": info, "count": count}

    html = get("https://www.sukl.cz/tydenni-zpravy-o-prijatych-hlasenich-podezreni-na-nezadouci")
    tbodies = Soup(html).find("tbody")
    date_for = datetime.strptime(tbodies[0].find("td")[2].text, "%d.%m.%Y")
    submits = int(tbodies[0].find("td")[3].text)
    submit_details_df = pd.DataFrame([parse_effect(tr) for tr in tbodies[1].find("tr")[1:]])

    submit_details_df["timestamp"] = timestamp

    submit_old = db.query(Submit).order_by(desc(Submit.date_for)).first()

    if submit_old is None or submit_old.date_for < date_for:
        db.add(Submit(timestamp, date_for, submits))
        db.commit()


def get_vaccinations(timestamp):
    vaccines = pd.read_csv(
        "https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/ockovani.csv",
        parse_dates=["datum"],
        infer_datetime_format=True,
    )
    vaccines = vaccines.groupby("datum", as_index=False)[["prvnich_davek", "druhych_davek"]].sum()
    vaccines.columns = ["date_for", "first_vaccines", "second_vaccines"]
    vaccines["timestamp"] = timestamp
    vaccines = vaccines[["timestamp", "date_for", "first_vaccines", "second_vaccines"]]
    vaccines.to_sql("vaccines", db.connection(), if_exists="replace", index=False)
    db.commit()


def get_deaths(timestamp):
    deaths = pd.read_csv(
        "https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/nakazeni-vyleceni-umrti-testy.csv",
        parse_dates=["datum"],
        infer_datetime_format=True,
    )
    deaths = deaths[["datum", "kumulativni_pocet_umrti"]]
    deaths.columns = ["date_for", "deads_cumulative"]
    deaths["timestamp"] = timestamp
    deaths = deaths[["timestamp", "date_for", "deads_cumulative"]]
    deaths.to_sql("deads", db.connection(), if_exists="replace", index=False)
    db.commit()


def get_cases(timestamp):
    cases = pd.read_csv(
        "https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/nakaza.csv",
        parse_dates=["datum"],
        infer_datetime_format=True,
    )
    cases.columns = ["date_for", "cases", "cases_cumulative"]
    cases["timestamp"] = timestamp
    cases = cases[["timestamp", "date_for", "cases", "cases_cumulative"]]
    cases.to_sql("cases", db.connection(), if_exists="replace", index=False)
    db.commit()


def update():
    timestamp = datetime.now()
    get_submits(timestamp)
    get_vaccinations(timestamp)
    get_deaths(timestamp)
    get_cases(timestamp)


if __name__ == "__main__":
    update()
