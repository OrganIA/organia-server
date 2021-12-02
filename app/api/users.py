from typing import List
from fastapi import APIRouter

from app import db
from app.errors import InvalidRequest, NotFoundError
from app.models import User
from app.api.schemas.user import UserSchema, UserCreateSchema, UserUpdateSchema
from . import permissions
from .dependencies import logged_user


router = APIRouter(prefix='/users')


@router.get('/', response_model=List[UserSchema])
async def get_users():
    return db.session.query(User).all()


@router.get('/me', response_model=UserSchema)
async def get_me(logged_user=logged_user):
    return logged_user


@router.get('/{user_id}', response_model=UserSchema)
async def get_user(user_id: int):
    return db.session.get(User, user_id) or NotFoundError.r()


@router.post('/', status_code=201, response_model=UserSchema)
async def create_user(data: UserCreateSchema, logged_user=logged_user):
    permissions.users.can_edit(logged_user)
    print(data)
    try:
        user = User.from_data(data)
    except Exception as error:
        raise InvalidRequest
    db.session.add(user)
    db.session.commit()
    return user


@router.post('/{user_id}', response_model=UserSchema)
async def update_user(
    user_id: int, data: UserUpdateSchema, logged_user=logged_user
):
    permissions.users.can_edit(logged_user)
    user = await get_user(user_id)
    user.update(data)
    db.session.commit()
    return user


@router.delete('/{user_id}')
async def delete_user(user_id: int, logged_user=logged_user):
    permissions.users.can_edit(logged_user)
    user = await get_user(user_id)
    db.session.delete(user)
    db.session.commit()
