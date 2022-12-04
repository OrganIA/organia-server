from app import auth, db
from app.db.models import User
from app.errors import NotFoundError, Unauthorized
from app.utils.bp import Blueprint

bp = Blueprint(__name__)


@bp.get('/')
def get_users(data: list[int]):
    query = db.session.query(User)
    if data:
        query = query.filter(User.id.in_(data))
    return query


@bp.get('/me')
@auth.route()
def get_me(auth_user: User):
    return auth_user


@bp.get('/<int:user_id>')
def get_user(user_id: int):
    return db.session.get(User, user_id)


@bp.post('/<int:user_id>')
@auth.route()
def update_user(user_id: int, data: dict, auth_user: User):
    if (auth_user.role.can_edit_users or auth_user.id == user_id) is False:
        raise Unauthorized
    user = get_user(user_id)
    for key, value in data.items():
        setattr(user, key, value)
    db.session.commit()
    return user


@bp.delete('/<int:user_id>')
@auth.route(edit_users=True)
def delete_user(user_id: int, auth_user: User):
    user = db.session.get(User, user_id)
    if not user:
        raise NotFoundError
    db.session.delete(user)
    db.session.commit()
