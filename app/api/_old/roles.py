from typing import List
from fastapi import APIRouter

from app import db
from app.errors import AlreadyTakenError, NotFoundError, NotAcceptableError
from app.models import Role
from app.api.schemas.role import RoleSchema, RoleUpdateSchema, RoleCreateSchema
from . import permissions
from .dependencies import logged_user


router = APIRouter(prefix='/roles')


@router.get('/', response_model=List[RoleSchema])
async def get_roles():
    return db.session.query(Role).all()


@router.get('/{role_id}', response_model=RoleSchema)
async def get_role(role_id: int):
    return db.get(Role, role_id)


@router.post('/', status_code=201, response_model=RoleSchema)
async def create_role(data: RoleCreateSchema, logged_user=logged_user):
    permissions.roles.can_edit(logged_user)
    if db.session.query(Role).filter_by(name=data.name).first():
        raise AlreadyTakenError("name", data.name)
    role = db.add(Role, data.dict(), author=logged_user)
    return role


@router.post('/{role_id}', response_model=RoleSchema)
async def update_role(
    role_id: int, data: RoleUpdateSchema, logged_user=logged_user
):
    role = await get_role(role_id)
    permissions.roles.can_edit(logged_user)
    if db.session.query(Role).filter_by(name=data.name).first():
        raise AlreadyTakenError("name", data.name)
    db.edit(role, data.dict(exclude_unset=True), author=logged_user)
    return role


@router.delete('/{role_id}')
async def delete_role(role_id: int, logged_user=logged_user):
    permissions.roles.can_edit(logged_user)
    role = await get_role(role_id)
    if not role:
        raise NotFoundError()
    elif role.users:
        raise NotAcceptableError(
            "Please remove or update all users who have this role before"
            " removing it."
        )
    db.delete(role, author=logged_user)
