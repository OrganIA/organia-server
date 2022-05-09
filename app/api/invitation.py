from typing import List
from fastapi import APIRouter

from app import db
from app.errors import InvalidRequest
from app.api.schemas.user import UserSchema, UserCreateSchema
from app.models import Invitation, InvitationSchema, InvitationCreateSchema
from app.api.users import create_user


router = APIRouter(prefix='/invitations')


@router.get('/', response_model=List[InvitationSchema])
async def get_invitations():
    return db.session.query(Invitation).all()


# @router.get('/{invite_user_id}', response_model=InvitationSchema)
# async def get_invitation_by_invite_user(invite_user_id: int):
#     return db.session.get(Invitation, invite_user_id) or NotFoundError.r()

# @router.get('/{user_id}', response_model=InvitationSchema)
# async def get_invitation_by_user(user_id: int):
#     return db.session.get(Invitation, user_id) or NotFoundError.r()

@router.post('/', status_code=201, response_model=InvitationSchema)
async def create_invitation(invitation: InvitationCreateSchema):
    invitation = Invitation(author_id=invitation.user_id)
    db.session.add(invitation)
    db.session.commit()
    return invitation


@router.post('/{invite_token}', status_code=201, response_model=UserSchema)
async def create_invite_user(user: UserCreateSchema, invite_token: str):
    if not Invitation.get_from_invitation(invite_token):
        raise InvalidRequest('Invalid Token')
    return await create_user(user)
