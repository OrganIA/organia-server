import enum
import sqlalchemy as sa
from sqlalchemy import orm

from app import db
from app.helpers.enums import EnumStr


class ActionLog(db.CreatedMixin, db.Base):
    class ActionType(EnumStr):
        create = enum.auto()
        delete = enum.auto()
        edit = enum.auto()

    action = sa.Column(sa.Enum(ActionType), nullable=False)
    target_type = sa.Column(sa.String)
    target_id = sa.Column(sa.Integer)
    properties = sa.Column(sa.String)
    message = sa.Column(sa.String)
    author_id = sa.Column(sa.ForeignKey('users.id'))

    author = orm.relationship('User', backref='actions')

    def __str__(self):
        return (
            f'Action "{self.action.value}"'
            f' for {self.target_type}#{self.target_id}:'
            f' "{self.message}" (props {self.properties}) '
            f' by {self.author}'
        )
