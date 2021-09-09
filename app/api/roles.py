from typing import List
from fastapi import APIRouter

from app import db
from app.errors import NotFoundError
from app.models import Role
from app.api.schemas.role import RoleSchema, RoleCreateSchema, RoleUpdateSchema
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
async def create_role(data: RoleCreateSchema):
    role = Role.from_data(data)
    db.session.add(role)
    db.session.commit()
    return role


# @router.post('/{role_id}', response_model=RoleSchema)
# async def update_role(
#     role_id: int, data: RoleUpdateSchema, logged_user=logged_user
# ):
#     role = await get_role(role_id)
#     permissions.users.can_edit(logged_user, user)
#     role.update(data)
#     db.session.commit()
#     return role


# @router.delete('/{role_id}')
# async def delete_role(role_id: int):
#     role = await get_role(role_id)
#     db.session.delete(role)
#     db.session.commit()
