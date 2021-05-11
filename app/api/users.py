from fastapi import APIRouter

from app import db
from app.errors import AlreadyTakenError
from app.models import User, UserCreateSchema, UserUpdateSchema


router = APIRouter(prefix='/users')


@router.get('/')
async def get_users():
    return db.session.query(User).all()


@router.get('/{user_id}')
async def get_user(user_id: int):
    return db.get_or_404(User, user_id)


@router.post('/', status_code=201)
async def create_user(user: UserCreateSchema):
    AlreadyTakenError.check(User, 'email', user.email)
    user = User(name=user.name, email=user.email)
    db.session.add(user)
    db.session.commit()
    return await get_user(user.id)


@router.post('/{user_id}')
async def update_user(user_id: int, data: UserUpdateSchema):
    user = await get_user(user_id)
    user.update(data, update_schema=True)
    db.session.commit()
    return await get_user(user_id)


@router.delete('/{user_id}')
async def delete_user(user_id: int):
    user = await get_user(user_id)
    db.session.delete(user)
    db.session.commit()
