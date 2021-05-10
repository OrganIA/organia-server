import sqlalchemy as sa
from app.db import Base, TimedMixin, Schema


class User(TimedMixin, Base):
    name = sa.Column(sa.String, nullable=False)
    email = sa.Column(sa.String, nullable=False, unique=True)


class UserSchema(Schema):
    name: str
    email: str

    class Config:
        orm_mode = True


class UserCreateSchema(Schema):
    name: str
    email: str
    # password: str
