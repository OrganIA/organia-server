import sqlalchemy as sa
from sqlalchemy import orm

from app import db


class ChatMember(db.Base):
    id = None
    chat_id = sa.Column(sa.Integer, sa.ForeignKey("chats.id"), primary_key=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey("users.id"), primary_key=True)


class Chat(db.mixins.TimedMixin, db.Base):
    __AUTO_DICT_EXCLUDE__ = ['creator_id']
    __AUTO_DICT_INCLUDE__ = ['users', 'creator']

    name = sa.Column(sa.String, default="Nouvelle conversation", nullable=False)
    creator_id = sa.Column(sa.ForeignKey('users.id'))

    creator = orm.relationship("User", back_populates="created_chats")
    users = orm.relationship(
        "User", secondary="chat_members", back_populates="chats"
    )
    messages = orm.relationship("Message", back_populates="chat")
