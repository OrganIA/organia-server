from typing import List
from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from app import db
from app.errors import AlreadyTakenError, NotFoundError
from app.models import Role
from app.api.schemas.role import RoleSchema, RoleUpdateSchema
from . import permissions
from .dependencies import logged_user


router = APIRouter(prefix='/roles')


@router.get('/', response_model=List[RoleSchema])
async def get_roles():
    return db.session.query(Role).all()


@router.get('/{role_id}', response_model=RoleSchema)
async def get_role(role_id: int):
    return db.session.get(Role, role_id) or NotFoundError.r()


@router.post('/', status_code=201, response_model=RoleSchema)
async def create_role(data: RoleSchema, logged_user=logged_user):
    permissions.roles.can_edit(logged_user)
    if db.session.query(Role).filter_by(name=data.name).first():
        raise AlreadyTakenError("name", data.name)
    role = Role.from_data(data)
    db.session.add(role)
    db.session.commit()
    return role


@router.post('/{role_id}', response_model=RoleSchema)
async def update_role(
    role_id: int, data: RoleUpdateSchema, logged_user=logged_user
):
    role = await get_role(role_id)
    permissions.roles.can_edit(logged_user)
    if db.session.query(Role).filter_by(name=data.name).first():
        raise AlreadyTakenError("name", data.name)
    role.update(data)
    db.session.commit()
    return role


@router.delete('/{role_id}')
async def delete_role(role_id: int, logged_user=logged_user):
    role = await get_role(role_id)
    permissions.roles.can_edit(logged_user)
    db.session.delete(role)
    db.session.commit()
