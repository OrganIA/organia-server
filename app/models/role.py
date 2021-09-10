from typing import Optional
import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.sql.expression import null

from app import db
from app.errors import AlreadyTakenError, PasswordMismatchError


class Role(db.TimedMixin, db.Base):
    name = sa.Column(sa.String, nullable=False, unique=True)
    can_manage_users = sa.Column(sa.Boolean, default=False, nullable=False)
    can_manage_persons = sa.Column(sa.Boolean, default=False, nullable=False)
    can_manage_roles = sa.Column(sa.Boolean, default=False, nullable=False)
    can_manage_hospitals = sa.Column(sa.Boolean, default=False, nullable=False)
    can_invite = sa.Column(sa.Boolean, default=False, nullable=False)

    users = orm.relationship('User', back_populates='role')

    @classmethod
    def get_default_role(cls):
        if not (role := db.session.query(cls)
                .filter_by(name="default").first()):
            role = cls(name="default")
            db.session.add(role)
            db.session.commit()
        return role
