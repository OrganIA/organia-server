import sqlalchemy as sa

from app import db
from app.db.mixins import OrganMixin


class Liver(OrganMixin, db.Base):
    tumors_count = sa.Column(sa.Integer, default=0)
    biggest_tumor_size = sa.Column(sa.Integer)
    alpha_fetoprotein = sa.Column(sa.Integer)
