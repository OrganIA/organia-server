import sqlalchemy as sa
from sqlalchemy import orm

from app import db


class Role(db.Base):
    can_edit_users = sa.Column(sa.Boolean, default=False)
    can_edit_hospitals = sa.Column(sa.Boolean, default=False)
    can_edit_listings = sa.Column(sa.Boolean, default=False)
    can_edit_staff = sa.Column(sa.Boolean, default=False)
    can_edit_roles = sa.Column(sa.Boolean, default=False)
    can_edit_persons = sa.Column(sa.Boolean, default=False)
    can_invite = sa.Column(sa.Boolean, default=False)
    name = sa.Column(sa.String, nullable=False, unique=True)

    user = orm.relationship('User', back_populates='role')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'can_edit_users': self.can_edit_users,
            'can_edit_hospitals': self.can_edit_hospitals,
            'can_edit_listings': self.can_edit_listings,
            'can_edit_staff': self.can_edit_staff,
            'can_edit_roles': self.can_edit_roles,
            'can_edit_persons': self.can_edit_persons,
            'can_invite': self.can_invite,
        }
