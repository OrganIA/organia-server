from typing import Optional
import sqlalchemy as sa
from app import db
from app.errors import AlreadyTakenError


class User(db.TimedMixin, db.Base):
    name = sa.Column(sa.String, nullable=False)
    email = sa.Column(sa.String, nullable=False, unique=True)

    @db.Base.updater('email')
    def set_unique_email(self, value):
        AlreadyTakenError.check(
            type(self), 'email', value, type(self).id != self.id
        )
        self.email = value


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
