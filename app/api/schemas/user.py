from typing import Optional

from app import db
from .role import RoleSchema


class UserSchema(db.TimedMixin.Schema):
    email: str
    role_id: int

    class Config:
        orm_mode = True


class UserCreateSchema(db.Schema):
    email: str
    password: str


class UserUpdateSchema(db.Schema):
    email: Optional[str]
    password: Optional[str]

