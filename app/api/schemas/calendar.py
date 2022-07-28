from datetime import datetime
from typing import Optional
from app import db
from .user import UserSchema


class CalendarEventSchema(db.CreatedMixin.Schema):
    start_date: datetime
    end_date: datetime
    title: str
    description: Optional[str]
    typerdv: str
    author: Optional[UserSchema]

    class Config:
        orm_mode = True


class CalendarEventCreateSchema(db.Schema):
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    title: Optional[str]
    description: Optional[str]
    typerdv: Optional[str]
