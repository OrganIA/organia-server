from datetime import date
from typing import Optional

from app import db
from app.models import Role


class RoleSchema(db.Schema):
    can_manage_users: bool
    can_manage_persons: bool
    can_manage_roles: bool
    can_manage_hospitals: bool
    can_invite: bool
    class Config:
        orm_mode = True


class RoleGetSchema(RoleSchema, db.TimedMixin.Schema):
    can_manage_users: bool
    can_manage_persons: bool
    can_manage_roles: bool
    can_manage_hospitals: bool
    can_invite: bool


class RoleUpdateSchema(RoleSchema):
    can_manage_users: bool
    can_manage_persons: bool
    can_manage_roles: bool
    can_manage_hospitals: bool
    can_invite: bool
