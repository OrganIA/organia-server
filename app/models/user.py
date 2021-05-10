from typing import Optional
import sqlalchemy as sa
from app.db import Base, TimedMixin, Schema
from app.errors import AlreadyTakenError


class User(TimedMixin, Base):
    name = sa.Column(sa.String, nullable=False)
    email = sa.Column(sa.String, nullable=False, unique=True)

    @Base.updater('email')
    def set_unique_email(self, value):
        AlreadyTakenError.check(
            type(self), 'email', value, type(self).id != self.id
        )
        self.email = value


class UserSchema(TimedMixin.Schema):
    name: str
    email: str

    class Config:
        orm_mode = True


class UserCreateSchema(Schema):
    name: str
    email: str
    # password: str


class UserUpdateSchema(Schema):
    name: Optional[str]
    email: Optional[str]
