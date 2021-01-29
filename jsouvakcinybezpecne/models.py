from . import db

class Stat(db.Model):
    
    __tablename = 'stats'

    date_from = db.Column(
        db.String(64),
        primary_key=True
    )

    date_to = db.Column(
        db.String(64),
        index=False,
        unique=False,
        nullable=False
    )

    vaccinated = db.Column(
        db.Integer,
        index=False,
        unique=False,
        nullable=False
    )

    def __repr__(self):
        return f'<Stat from {self.date_from} to {self.date_to}>'
