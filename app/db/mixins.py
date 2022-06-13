from datetime import datetime
import sqlalchemy as sa
from sqlalchemy import orm


@orm.declarative_mixin
class IdMixin:
    id = sa.Column(sa.Integer, primary_key=True)


@orm.declarative_mixin
class CreatedMixin(IdMixin):
    created_at = sa.Column(sa.DateTime, default=datetime.utcnow)


@orm.declarative_mixin
class TimedMixin(CreatedMixin):
    updated_at = sa.Column(sa.DateTime, onupdate=datetime.utcnow)


@orm.declarative_mixin
class DurationMixin(IdMixin):
    start_date = sa.Column(sa.Date)
    end_date = sa.Column(sa.Date)
