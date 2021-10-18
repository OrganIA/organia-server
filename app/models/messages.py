import sqlalchemy as sa
from sqlalchemy import orm

from app import db


class Message(db.TimedMixin, db.Base):
    content = sa.Column(sa.String, nullable=False)
    chat = sa.Column(sa.ForeignKey('chats.id'))
    sender = sa.Column(sa.ForeignKey('users.id'))