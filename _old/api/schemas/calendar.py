from datetime import datetime
from typing import Optional

from app import db
from .user import UserSchema


class CalendarEventSchema(db.CreatedMixin.Schema):
    date: Optional[datetime]
    description: Optional[str]
    author: Optional[UserSchema]

    class Config:
        orm_mode = True


class CalendarEventCreateSchema(db.Schema):
    date: Optional[datetime]
    description: Optional[str]
