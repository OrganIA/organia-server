import sqlalchemy as sa
from sqlalchemy import orm

from app import db


class Chat(db.IdMixin, db.Base):
    messages = orm.relationship("Message", back_populates="chat")
    users = orm.relationship("ChatGroup", back_populates="chat")
    chat_name = sa.Column(sa.String, default="New Conversation", nullable=False)
    creator_id = sa.Column(sa.Integer)
