from typing import Optional
import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.sql.expression import null

from app import db
from app.errors import AlreadyTakenError, PasswordMismatchError


class Role(db.TimedMixin, db.Base):
    can_manage_users = sa.Column(sa.Boolean, default=False, nullable=False)
    can_manage_persons = sa.Column(sa.Boolean, default=False, nullable=False)
    can_manage_roles = sa.Column(sa.Boolean, default=False, nullable=False)
    can_manage_hospitals = sa.Column(sa.Boolean, default=False, nullable=False)
    can_invite = sa.Column(sa.Boolean, default=False, nullable=False)