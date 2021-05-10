from typing import List

from app import db
from app.models import User, UserSchema, UserCreateSchema
from . import router


@router.get('/', response_model=List[UserSchema])
async def users():
    return db.session.query(User).all()


@router.post('/', response_model=UserSchema, status_code=201)
async def create_user(user: UserCreateSchema):
    user = User(name=user.name, email=user.email)
    db.session.add(user)
    db.session.commit()
    return user
