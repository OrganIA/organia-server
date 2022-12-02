from app import db
from app.db.models import LoginToken, User
from app.errors import InvalidRequest
from app.utils.bp import Blueprint
from app.utils.static import Static

bp = Blueprint(__name__, auth=False)


class LoginSchema(Static):
    email = str
    password = str


class RegisterSchema(Static):
    __ERROR_ON_UNFOUND__ = False

    email = str
    password = str
    firstname = str
    lastname = str
    phone_number = str


@bp.post('/login')
def login(data: LoginSchema, user=None):
    user: User = (
        user or db.session.query(User).filter_by(email=data.email).first()
    )
    if not user:
        raise InvalidRequest("User not found")
    user.check_password(data.password)
    token = LoginToken.get_valid_for_user(user)
    db.session.commit()
    return {'token': token.value, 'user': user()}


@bp.post('/register', success=201)
def create_user(data: RegisterSchema):
    User.check_email(data.email)
    user = User(**data.dict)
    db.session.add(user)
    db.session.commit()
    return login(data=data, user=user)
