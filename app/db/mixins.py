from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel as Schema
import sqlalchemy as sa
from sqlalchemy import orm


@orm.declarative_mixin
class IdMixin:
    id = sa.Column(sa.Integer, primary_key=True)

    class Schema(Schema):
        id: int


@orm.declarative_mixin
class CreatedMixin(IdMixin):
    created_at = sa.Column(sa.DateTime, default=datetime.utcnow)

    class Schema(IdMixin.Schema):
        created_at: Optional[datetime]


@orm.declarative_mixin
class TimedMixin(CreatedMixin):
    updated_at = sa.Column(sa.DateTime, onupdate=datetime.utcnow)

    class Schema(CreatedMixin.Schema):
        updated_at: Optional[datetime]


@orm.declarative_mixin
class DurationMixin(IdMixin):
    start_date = sa.Column(sa.Date)
    end_date = sa.Column(sa.Date)

    class Schema(IdMixin.Schema):
        start_date: Optional[date]
        end_date: Optional[date]
