import sqlalchemy as sa
from sqlalchemy import orm

from app import db


class Chat(db.IdMixin, db.Base):
    messages = orm.relationship("Message", back_populates="chat")
    users = orm.relationship("ChatGroup", back_populates="chat")
