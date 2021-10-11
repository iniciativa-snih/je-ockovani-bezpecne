import pandas as pd
from gazpacho import get, Soup
from datetime import datetime
import json


def get_submits(timestamp):
    def is_int(s):
        try:
            int(s)
            return True
        except ValueError:
            return False

    def parse_effect(tr):
        effect = tr.find("p")[0].text
        info = tr.find("p")[1].text
        num = tr.find("p")[2]
        if is_int(num.text):
            count = int(num.text)
        else:
            span = num.find("span")
            if span is not None:
                count = int(span.text)
            else:
                count = 0
        return {"date_for": date_for, "effect": effect, "info": info, "count": count}

    def myconverter(o):
        if isinstance(o, datetime):
            return datetime.strftime(o, "%Y-%m-%d")

    html = get(
        "https://www.sukl.cz/tydenni-zpravy-o-prijatych-hlasenich-podezreni-na-nezadouci"
    )
    tbodies = Soup(html).find("tbody")
    date_for = datetime.strptime(tbodies[0].find("td")[2].text, "%d. %m. %Y")
    submits = int(tbodies[0].find("td")[3].text)
    with open("./data/submits.json", "w+") as f:
        json.dump({"date_for": date_for, "submits": submits}, f, default=myconverter)


def get_vaccinations(timestamp):
    vaccines = pd.read_csv(
        "https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/ockovani.csv",
        parse_dates=["datum"],
        infer_datetime_format=True,
    )
    vaccines = vaccines.groupby("datum", as_index=False)[
        ["prvnich_davek", "druhych_davek"]
    ].sum()
    vaccines["prvnich_davek"] = vaccines["prvnich_davek"].cumsum()
    vaccines["druhych_davek"] = vaccines["druhych_davek"].cumsum()
    vaccines.columns = ["date_for", "first_vaccines", "second_vaccines"]
    vaccines.sort_values("date_for", inplace=True)
    vaccines = vaccines[["date_for", "first_vaccines", "second_vaccines"]]
    vaccines.to_json("./data/vaccines.json", "records", date_format="iso", indent=2)


def get_stats(timestamp):
    cases = pd.read_csv(
        "https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/nakazeni-vyleceni-umrti-testy.csv",
        parse_dates=["datum"],
        infer_datetime_format=True,
    )
    cases = cases[
        [
            "datum",
            "kumulativni_pocet_nakazenych",
            "kumulativni_pocet_umrti",
            "kumulativni_pocet_testu",
        ]
    ]
    cases.columns = ["date_for", "cases", "deaths", "tests"]
    cases.sort_values("date_for", inplace=True)
    cases.to_json("./data/stats.json", "records", date_format="iso", indent=2)


def update(timestamp):
    get_submits(timestamp)
    get_vaccinations(timestamp)
    get_stats(timestamp)


if __name__ == "__main__":
    t = datetime.now()
    update(t)
