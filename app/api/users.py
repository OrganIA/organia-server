from app.db.models import User
from app import Blueprint, db, auth


bp = Blueprint(__name__)


@bp.get('/')
@auth.check()
def get_users(data: list[int]):
    query = db.session.query(User)
    if data:
        query = query.filter(User.id.in_(data))
    return query


@bp.get('/me')
@auth.check()
def get_me(auth_user: User):
    return auth_user


@bp.get('/<int:user_id>')
@auth.check()
def get_user(user_id: int):
    return db.get(User, user_id)


# @bp.post('/{user_id}', response_model=UserSchema)
# def update_user(
#     user_id: int, data: UserUpdateSchema, logged_user=logged_user
# ):
#     user = get_user(user_id)
#     permissions.users.can_edit(logged_user, user)
#     user.update(data)
#     db.session.commit()
#     return user


@bp.delete('/<int:user_id>')
@auth.check(manage_users=True)
def delete_user(user_id: int, auth_user: User):
    user = db.get(user_id)
    db.delete(user, author=auth_user)
