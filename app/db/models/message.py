import sqlalchemy as sa
from sqlalchemy import orm

from app import db


class Message(db.mixins.TimedMixin, db.Base):
    __AUTO_DICT_EXCLUDE__ = ['sender_id', 'chat_id']
    __AUTO_DICT_INCLUDE__ = ['sender', 'chat', 'user']
    content = sa.Column(sa.String, nullable=False)
    chat_id = sa.Column(sa.ForeignKey('chats.id'))
    sender_id = sa.Column(sa.ForeignKey('users.id'))

    sender = orm.relationship("User", back_populates="messages")
    chat = orm.relationship("Chat", back_populates="messages")

    def to_dict(self):
        return {
            "id": self.id,
            "content": self.content,
            "chat_id": self.chat_id,
            "sender": self.sender.to_dict(),
            "created_at": self.created_at,
        }
