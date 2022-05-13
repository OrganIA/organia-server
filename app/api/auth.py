from fastapi import APIRouter, Depends

from app import db
from app.errors import InvalidRequest
from app.models import LoginToken, User
from app.api.dependencies import get_db
from app.api.schemas.user import UserSchema

router = APIRouter(prefix='/auth')


class LoginSchema(db.Schema):
    email: str
    password: str


@router.post('/')
async def login(data: LoginSchema, session=Depends(get_db)):
    """
    Raises a 401 for invalid password and 404 for non-existing user
    """
    user: User = (
        session.query(User).filter_by(email=data.email).first()
        or InvalidRequest.r('User not found')
    )
    user.check_password(data.password)
    token = LoginToken.get_valid_for_user(user)
    session.commit()
    return {'token': token.value, 'user': UserSchema.from_orm(user)}
