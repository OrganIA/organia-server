from fastapi import APIRouter

from app import db
from app.errors import InvalidRequest
from app.api.schemas.user import UserSchema, UserCreateSchema
from app.models import Invitation, User
from app.api.users import create_user
from .dependencies import logged_user


router = APIRouter(prefix='/invitations')


# @router.get('/', response_model=List[InvitationSchema])
# async def get_invitations():
#     return db.session.query(Invitation).all()


# @router.get('/{invite_user_id}', response_model=InvitationSchema)
# async def get_invitation_by_invite_user(invite_user_id: int):
#     return db.session.get(Invitation, invite_user_id) or NotFoundError.r()

# @router.get('/{user_id}', response_model=InvitationSchema)
# async def get_invitation_by_user(user_id: int):
#     return db.session.get(Invitation, user_id) or NotFoundError.r()

@router.post('/', status_code=201)
async def create_invitation(logged_user: User = logged_user):
    invitation = Invitation(author_id=logged_user.id)
    db.session.add(invitation)
    db.session.commit()
    return str(invitation)


@router.post('/{invite_token}', status_code=201, response_model=UserSchema)
async def create_invite_user(user: UserCreateSchema, invite_token: str):
    if not Invitation.get_from_token(invite_token):
        raise InvalidRequest('Invalid Token')
    return await create_user(user)
