import sqlalchemy as sa
from app.db import Base, TimedMixin


class User(TimedMixin, Base):
    name = sa.Column(sa.String, nullable=False)
    email = sa.Column(sa.String, nullable=False, unique=True)
