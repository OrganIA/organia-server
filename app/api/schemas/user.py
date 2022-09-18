from typing import Optional

from app import db


class UserSchema(db.TimedMixin.Schema):
    email: str
    firstname: str
    lastname: str
    phone_number: str
    role_id: int

    class Config:
        orm_mode = True


class UserCreateSchema(db.Schema):
    email: str
    password: str
    firstname: str
    lastname: str
    phone_number: Optional[str]
    country_code: Optional[str]
    role_id: Optional[int]


class UserUpdateSchema(db.Schema):
    email: Optional[str]
    password: Optional[str]
    firstname: Optional[str]
    lastname: Optional[str]
    phone_number: Optional[str]
    country_code: Optional[str]
    role_id: Optional[int]
