from fastapi import APIRouter

from app import db
from app.errors import InvalidRequest
from app.models import LoginToken, User
from app.api.schemas.user import UserSchema

router = APIRouter(prefix='/auth')


class LoginSchema(db.Schema):
    email: str
    password: str


@router.post('/')
async def login(data: LoginSchema):
    """
    Raises a 401 for invalid password and 404 for non-existing user
    """
    user: User = (
        db.session.query(User).filter_by(email=data.email).first()
        or InvalidRequest.r('User not found')
    )
    user.check_password(data.password)
    token = LoginToken.get_valid_for_user(user)
    db.session.commit()
    return {'token': token.value, 'user': UserSchema.from_orm(user)}
