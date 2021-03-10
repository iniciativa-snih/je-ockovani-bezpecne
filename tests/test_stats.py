from gazpacho import Soup
from datetime import datetime


def test_index(client):
    from jeockovanibezpecne.init import fmt_date

    soup = Soup(client.get("/").data.decode("utf8"))

    assert soup.find("p", {"class": "count vaccine-deaths"}).text == "0"
    assert soup.find("p", {"class": "count vaccinated"}).text == "450"
    assert soup.find("p", {"class": "count covid-infected"}).text == "180"
    assert soup.find("p", {"class": "count covid-deaths"}).text == "200"
    assert soup.find("time").text == fmt_date(datetime(2021, 3, 10))
