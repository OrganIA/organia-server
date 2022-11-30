import sqlalchemy as sa
from sqlalchemy import orm

from app import db


class ChatMember(db.Base):
    id = None
    chat_id = sa.Column(sa.Integer, sa.ForeignKey("chats.id"), primary_key=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey("users.id"), primary_key=True)


class Chat(db.mixins.TimedMixin, db.Base):
    name = sa.Column(sa.String, default="Nouvelle conversation", nullable=False)
    creator_id = sa.Column(sa.ForeignKey('users.id'))

    creator = orm.relationship("User", back_populates="created_chats")
    users = orm.relationship(
        "User", secondary="chat_members", back_populates="chats"
    )
    messages = orm.relationship("Message", back_populates="chat")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "creator_id": self.creator_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "users": self.users,
        }
