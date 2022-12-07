import sqlalchemy as sa
from sqlalchemy import orm

from app import db


class Kidney(db.Base):
    listing_id = sa.Column(sa.ForeignKey("listings.id"))

    is_dialyse = sa.Column(sa.Boolean, default=False, nullable=True)
    is_retransplantation = sa.Column(sa.Boolean, default=False, nullable=True)
    start_date_dialyse = sa.Column(sa.Date, nullable=True)
    EndDateDialyse = sa.Column(sa.Date, nullable=True)
    arf_date = sa.Column(sa.Date, nullable=True)
    date_transplantation = sa.Column(sa.Date, nullable=True)
    re_registration_date = sa.Column(sa.Date, nullable=True)

    listing = orm.relationship(
        'Listing', back_populates="kidney", uselist=False
    )
