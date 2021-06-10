from typing import Optional
import sqlalchemy as sa
from sqlalchemy import orm
from passlib.context import CryptContext

from app import db
from app.errors import AlreadyTakenError, PasswordMismatchError


class User(db.TimedMixin, db.Base):
    PASSWORD_CONTEXT = CryptContext(schemes=['bcrypt'], deprecated='auto')
    UPDATERS = {
        'email': 'get_unique_email',
        'password': 'get_hashed_password'
    }

    email = sa.Column(sa.String, nullable=False, unique=True)
    password = sa.Column(sa.String)

    person = orm.relationship('Person', uselist=False, back_populates='user')

    @classmethod
    def get_unique_email(cls, value, obj=None):
        AlreadyTakenError.check(
            cls, 'email', value,
            filters=cls.id != obj.id if obj else None,
        )
        return value

    @classmethod
    def get_hashed_password(cls, value):
        return cls.PASSWORD_CONTEXT.hash(value)

    def check_password(self, password, exc=True):
        result = self.PASSWORD_CONTEXT.verify(password, self.password)
        if not result and exc:
            raise exc if isinstance(exc, Exception) else PasswordMismatchError
        return result


class UserSchema(db.TimedMixin.Schema):
    email: str

    class Config:
        orm_mode = True


class UserCreateSchema(db.Schema):
    email: str
    password: str


class UserUpdateSchema(db.Schema):
    email: Optional[str]
    password: Optional[str]
