import sqlalchemy as sa
from sqlalchemy import orm

from app import db


class Message(db.TimedMixin, db.Base):
    content = sa.Column(sa.String, nullable=False)
    chat_id = sa.Column(sa.ForeignKey('chats.id'))
    sender_id = sa.Column(sa.ForeignKey('users.id'))
    
    sender = orm.relationship("User", back_populates="messages")
    chat = orm.relationship("Chat", back_populates="messages")