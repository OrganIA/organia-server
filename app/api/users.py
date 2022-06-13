from app.errors import InvalidRequest, NotFoundError, AlreadyTakenError
from app.db.models import User, Role
from app import Blueprint, Flask, Static, db


bp = Blueprint(__name__)


# @bp.get('/', response_model=List[UserSchema])
# def get_users():
#     return db.session.query(User).all()


# @bp.get('/me', response_model=UserSchema)
# def get_me(logged_user=logged_user):
#     return logged_user


# @bp.get('/{user_id}', response_model=UserSchema)
# def get_user(user_id: int):
#     return db.session.get(User, user_id) or NotFoundError.r()


class UserCreateSchema(Static):
    email = str
    password = str


@bp.post('/', success=201)
def create_user(data: UserCreateSchema):
    User.get_unique_email(data.email)
    user = User(**data.dict)
    db.session.add(user)
    db.session.commit()
    return user


# @bp.post('/{user_id}', response_model=UserSchema)
# def update_user(
#     user_id: int, data: UserUpdateSchema, logged_user=logged_user
# ):
#     user = get_user(user_id)
#     permissions.users.can_edit(logged_user, user)
#     user.update(data)
#     db.session.commit()
#     return user


# @bp.delete('/{user_id}')
# def delete_user(user_id: int, logged_user=logged_user):
#     user = get_user(user_id)
#     permissions.users.can_edit(logged_user, user)
#     db.session.delete(user)
#     db.session.commit()
