from app import db
from app.errors import AlreadyTakenError
from app.models import User, UserCreateSchema
from . import router


@router.get('/')
async def get_users():
    return db.session.query(User).all()


@router.get('/{user_id}')
async def get_user(user_id: int):
    return db.session.query(User).get(user_id)


@router.post('/', status_code=201)
async def create_user(user: UserCreateSchema):
    AlreadyTakenError.check(User, 'email', user.email)
    user = User(name=user.name, email=user.email)
    db.session.add(user)
    db.session.commit()
    return db.session.query(User).get(user.id)
