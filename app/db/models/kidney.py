import sqlalchemy as sa

from app import db


class Kidney(db.Base):
    listing_id = sa.Column(sa.ForeignKey("listings.id"))

    isDialyse = sa.Column(sa.Boolean, default=False, nullable=True)
    isRetransplantation = sa.Column(sa.Boolean, default=False, nullable=True)
    startDateDialyse = sa.Column(sa.Date, nullable=True)
    EndDateDialyse = sa.Column(sa.Date, nullable=True)
    ARFDate = sa.Column(sa.Date, nullable=True)
    DateTransplantation = sa.Column(sa.Date, nullable=True)
    ReRegistrationDate = sa.Column(sa.Date, nullable=True)

    score = sa.Column(sa.Float, nullable=True, default=0)