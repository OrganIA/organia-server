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
        role = db.session.query(cls).filter_by(name="default").first()
        return role

    @classmethod
    def get_admin_role(cls):
        role = db.session.query(cls).filter_by(name="admin").first()
        return role

    @classmethod
    def setup_roles(cls):
        cls.setup_admin_role()
        cls.setup_default_role()

    @classmethod
    def setup_admin_role(cls):
        if db.session.query(cls).filter_by(name="admin").first():
            return
        role = cls(name="admin", can_manage_users=True, can_manage_persons=True,
                   can_manage_roles=True, can_manage_hospitals=True,
                   can_invite=True)
        db.session.add(role)
        db.session.commit()

    @classmethod
    def setup_default_role(cls):
        if db.session.query(cls).filter_by(name="default").first():
            return
        role = cls(name="default")
        db.session.add(role)
        db.session.commit()
