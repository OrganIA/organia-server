from typing import List
from fastapi import APIRouter

from app import db
from app.errors import InvalidRequest, NotFoundError, AlreadyTakenError
from app.models import User, Role
from app.api.schemas.user import UserSchema, UserCreateSchema, UserUpdateSchema
from . import permissions
from .dependencies import logged_user


router = APIRouter(prefix='/users')


@router.get('/', response_model=List[UserSchema])
async def get_users():
    users = db.session.query(User).all()
    for user in users:
        user.phone_number = user._phone_number.international
    return users


@router.get('/me', response_model=UserSchema)
async def get_me(logged_user=logged_user):
    logged_user.phone_number = logged_user._phone_number.international
    return logged_user


@router.get('/{user_id}', response_model=UserSchema)
async def get_user(user_id: int):
    user =  db.session.get(User, user_id)
    if (user is not None):
        user.phone_number = user._phone_number.international
        return user
    else:
        return NotFoundError.r()


@router.post('/', status_code=201, response_model=UserSchema)
async def create_user(data: UserCreateSchema):
    try:
        role = db.get(Role, data.role_id)
    except Exception as e:
        Role.setup_roles()
    user = db.session.query(User).filter_by(email=data.email).first()
    if user:
        raise AlreadyTakenError("email", data.email)
    try:
        user = User.from_data(data)
    except Exception as e:
        raise InvalidRequest from e
    db.session.add(user)
    db.session.commit()
    return user


@router.post('/{user_id}', response_model=UserSchema)
async def update_user(
    user_id: int, data: UserUpdateSchema, logged_user=logged_user
):
    user = await get_user(user_id)
    permissions.users.can_edit(logged_user, user)
    if user.email == data.email:
        del data.email
    user.update(data)
    db.session.commit()
    return user


@router.delete('/{user_id}')
async def delete_user(user_id: int, logged_user=logged_user):
    user = await get_user(user_id)
    permissions.users.can_edit(logged_user, user)
    db.session.delete(user)
    db.session.commit()
