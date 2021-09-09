from datetime import date
from typing import Optional

from app import db
from app.models import Role


class RoleSchema(db.Schema):
    name: str
    can_manage_users: bool
    can_manage_persons: bool
    can_manage_roles: bool
    can_manage_hospitals: bool
    can_invite: bool
    class Config:
        orm_mode = True

class RoleCreateSchema(db.Schema):
    name: str
    can_manage_users: bool
    can_manage_persons: bool
    can_manage_roles: bool
    can_manage_hospitals: bool
    can_invite: bool


class RoleGetSchema(RoleSchema, db.TimedMixin.Schema):
    name: str
    can_manage_users: bool
    can_manage_persons: bool
    can_manage_roles: bool
    can_manage_hospitals: bool
    can_invite: bool


class RoleUpdateSchema(RoleSchema):
    name: str
    can_manage_users: bool
    can_manage_persons: bool
    can_manage_roles: bool
    can_manage_hospitals: bool
    can_invite: bool