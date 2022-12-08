import sqlalchemy as sa

from app import db
from app.db.mixins import OrganMixin


class Kidney(OrganMixin, db.Base):

    is_dialyse = sa.Column(sa.Boolean, default=False)
    is_retransplantation = sa.Column(sa.Boolean, default=False)
    start_date_dialyse = sa.Column(sa.Date)
    arf_date = sa.Column(sa.Date)
    date_transplantation = sa.Column(sa.Date)
    re_registration_date = sa.Column(sa.Date)
