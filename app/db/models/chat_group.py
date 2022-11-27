import sqlalchemy as sa
from sqlalchemy import orm

from app import db


class ChatGroup(db.Base):
    chat_id = sa.Column(sa.ForeignKey('chats.id'), nullable=False)
    user_id = sa.Column(sa.ForeignKey('users.id'), nullable=False)

    chat = orm.relationship("Chat", back_populates="groups")
    user = orm.relationship("User", back_populates="groups")
