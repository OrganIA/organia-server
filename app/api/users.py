from typing import List
from fastapi import APIRouter

from app import db
from app.errors import AlreadyTakenError, NotFoundError
from app.models import User, UserSchema, UserCreateSchema, UserUpdateSchema


router = APIRouter(prefix='/users')


@router.get('/', response_model=List[UserSchema])
async def get_users():
    return db.session.query(User).all()


@router.get('/{user_id}', response_model=UserSchema)
async def get_user(user_id: int):
    return db.session.get(User, user_id) or NotFoundError.r()


@router.post('/', status_code=201, response_model=UserSchema)
async def create_user(user: UserCreateSchema):
    AlreadyTakenError.check(User, 'email', user.email)
    user = User(name=user.name, email=user.email)
    db.session.add(user)
    db.session.commit()
    return await get_user(user.id)


@router.post('/{user_id}', response_model=UserSchema)
async def update_user(user_id: int, data: UserUpdateSchema):
    user = await get_user(user_id)
    user.update(data)
    db.session.commit()
    return await get_user(user_id)


@router.delete('/{user_id}')
async def delete_user(user_id: int):
    user = await get_user(user_id)
    db.session.delete(user)
    db.session.commit()
