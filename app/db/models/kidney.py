import sqlalchemy as sa

from app import db
from app.db.mixins import OrganMixin


class Kidney(OrganMixin, db.Base):
    is_under_dialysis = sa.Column(sa.Boolean, default=False)
    is_retransplantation = sa.Column(sa.Boolean, default=False)
    dialysis_start_date = sa.Column(sa.Date)
    dialysis_end_date = sa.Column(sa.Date)
    arf_date = sa.Column(sa.Date)
    date_transplantation = sa.Column(sa.Date)
    re_registration_date = sa.Column(sa.Date)
    A = sa.Column(sa.Float)
    B = sa.Column(sa.Float)
    DR = sa.Column(sa.Float)
    DQ = sa.Column(sa.Float)
