from datetime import datetime
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
class TimedMixin(IdMixin):
    created_at = sa.Column(sa.DateTime, default=datetime.utcnow)
    updated_at = sa.Column(sa.DateTime, onupdate=datetime.utcnow)

    class Schema(IdMixin.Schema):
        created_at: Optional[datetime]
        updated_at: Optional[datetime]
