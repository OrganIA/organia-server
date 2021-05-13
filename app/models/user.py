from typing import Optional
import sqlalchemy as sa
from passlib.context import CryptContext

from app import db
from app.errors import AlreadyTakenError


class User(db.TimedMixin, db.Base):
    PASSWORD_CONTEXT = CryptContext(schemes=['bcrypt'], deprecated='auto')

    name = sa.Column(sa.String, nullable=False)
    email = sa.Column(sa.String, nullable=False, unique=True)
    password = sa.Column(sa.String)

    @db.Base.updater('email')
    def set_unique_email(self, value):
        AlreadyTakenError.check(
            type(self), 'email', value, type(self).id != self.id
        )
        self.email = value

    @db.Base.updater('password')
    def set_hashed_password(self, value):
        self.password = self.PASSWORD_CONTEXT.hash(value)

    def verify_password(self, password):
        return self.PASSWORD_CONTEXT.verify(password, self.password)


class UserSchema(db.TimedMixin.Schema):
    name: str
    email: str

    class Config:
        orm_mode = True


class UserCreateSchema(db.Schema):
    name: str
    email: str
    # password: str


class UserUpdateSchema(db.Schema):
    name: Optional[str]
    email: Optional[str]
