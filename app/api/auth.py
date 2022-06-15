from app import db, Static, Blueprint
from app.errors import InvalidRequest
from app.db.models import LoginToken, User


bp = Blueprint(__name__)


class LoginSchema(Static):
    email = str
    password = str


@bp.post('/login')
def login(data: LoginSchema, user=None):
    """
    Raises a 401 for invalid password and 404 for non-existing user
    """
    user: User = user or db.session.query(User).filter_by(email=data.email).first()
    if not user:
        raise InvalidRequest("User not found")
    user.check_password(data.password)
    token = LoginToken.get_valid_for_user(user)
    db.session.commit()
    return {'token': token.value, 'user': user}


@bp.post('/register', success=201)
def create_user(data: LoginSchema):
    User.check_email(data.email)
    user = db.add(User, data.dict)
    return login(data=data, user=user)
