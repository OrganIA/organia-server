from app import db, Static, Blueprint
from app.errors import InvalidRequest
from app.db.models import LoginToken, User


bp = Blueprint(__name__)


class LoginSchema(Static):
    email = str
    password = str


@bp.post('/')
def login(data: LoginSchema):
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
    return {'token': token.value, 'user': user}
