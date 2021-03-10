from sqlalchemy import Column, Integer, DateTime
from datetime import datetime

from .database import Base


class Submit(Base):
    __tablename__ = "submits"

    timestamp = Column(DateTime, index=False, unique=False, nullable=False)
    date_for = Column(DateTime, primary_key=True)
    submits = Column(Integer, index=False, unique=False, nullable=False)

    def __init__(self, timestamp: datetime, date_for: datetime, submits: int):
        self.timestamp = timestamp
        self.date_for = date_for
        self.submits = submits

    def __repr__(self):
        return f"<Submit {self.timestamp} from {self.date_for} with {self.submits} submits>"


class Vaccine(Base):
    __tablename__ = "vaccines"

    timestamp = Column(DateTime, index=False, unique=False, nullable=False)
    date_for = Column(DateTime, primary_key=True)
    first_vaccines = Column(Integer, index=False, unique=False, nullable=False)
    second_vaccines = Column(Integer, index=False, unique=False, nullable=False)

    def __init__(self, timestamp: datetime, date_for: datetime, first_vaccines: int, second_vaccines: int):
        self.timestamp = timestamp
        self.date_for = date_for
        self.first_vaccines = first_vaccines
        self.second_vaccines = second_vaccines

    def __repr__(self):
        return (
            f"<Vaccine {self.timestamp} from {self.date_for} with {self.first_vaccines} and "
            + f"{self.second_vaccines} vaccines"
        )


class Dead(Base):
    __tablename__ = "deads"

    timestamp = Column(DateTime, index=False, unique=False, nullable=False)
    date_for = Column(DateTime, primary_key=True)
    deads_cumulative = Column(Integer, index=False, unique=False, nullable=False)

    def __init__(self, timestamp: datetime, date_for: datetime, deads_cumulative: int):
        self.timestamp = timestamp
        self.date_for = date_for
        self.deads_cumulative = deads_cumulative

    def __repr__(self):
        return f"<Dead {self.timestamp} from {self.date_for} with {self.deads_cumulative} deaths"


class Case(Base):
    __tablename__ = "cases"

    timestamp = Column(DateTime, index=False, unique=False, nullable=False)
    date_for = Column(DateTime, primary_key=True)
    cases = Column(Integer, index=False, unique=False, nullable=False)
    cases_cumulative = Column(Integer, index=False, unique=False, nullable=False)

    def __init__(self, timestamp: datetime, date_for: datetime, cases: int, cases_cumulative: int):
        self.timestamp = timestamp
        self.date_for = date_for
        self.cases = cases
        self.cases_cumulative = cases_cumulative

    def __repr__(self):
        return f"<Case {self.timestamp} from {self.date_for} with {self.cases} cases"
