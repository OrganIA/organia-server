from typing import List
from fastapi import APIRouter

from app import db
from app.errors import NotFoundError
from app.models import Chat
from app.api.schemas.chat import ChatSchema, ChatCreateSchema
# from . import permissions
from .dependencies import logged_user


router = APIRouter(prefix='/chats')


@router.get('/', response_model=List[ChatSchema])
async def get_chats(logged_user=logged_user):
    print("CACAAAAAAAAAAAAAAA")
    print(logged_user.id)
    print("COCOOOOOOOOOOOOOOOOOO")
    result = db.session.query(Chat).filter_by(user_a_id=logged_user.id).all()
    result += db.session.query(Chat).filter_by(user_b_id=logged_user.id).all()
    return result


# @router.get('/me', response_model=UserSchema)
# async def get_me(logged_user=logged_user):
#     return logged_user


# @router.get('/{user_id}', response_model=UserSchema)
# async def get_user(user_id: int):
#     return db.session.get(User, user_id) or NotFoundError.r()


# @router.post('/', status_code=201, response_model=UserSchema)
# async def create_user(data: UserCreateSchema):
#     user = User.from_data(data)
#     db.session.add(user)
#     db.session.commit()
#     return user


# @router.post('/{user_id}', response_model=UserSchema)
# async def update_user(
#     user_id: int, data: UserUpdateSchema, logged_user=logged_user
# ):
#     user = await get_user(user_id)
#     permissions.users.can_edit(logged_user, user)
#     user.update(data)
#     db.session.commit()
#     return user


# @router.delete('/{user_id}')
# async def delete_user(user_id: int):
#     user = await get_user(user_id)
#     db.session.delete(user)
#     db.session.commit()
