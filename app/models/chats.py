import sqlalchemy as sa
from sqlalchemy import orm

from app import db


class Chat(db.IdMixin, db.Base):
    user_a = sa.Column(sa.ForeignKey('users.id'), nullable=False)
    user_b = sa.Column(sa.ForeignKey('users.id'), nullable=False)

    user = orm.relationship('User', back_populates='chats')
