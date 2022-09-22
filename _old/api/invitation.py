from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import db
from app.errors import InvalidRequest
from app.api.schemas.user import UserSchema, UserCreateSchema
from app.models import Invitation
from app.api.users import create_user
from .dependencies import get_db, get_user


router = APIRouter(prefix='/invitations')


class InvitationSchema(db.TimedMixin.Schema):
    author: UserSchema
    consumer: UserSchema
    value: str


# TODO: Protect against non-admin read
@router.get('/', response_model=List[InvitationSchema])
def get_invitations(session=Depends(get_db)):
    return session.query(Invitation).all()


@router.post('/', status_code=201, response_model=InvitationSchema)
def create_invitation(session=Depends(get_db), user=Depends(get_user)):
    invitation = Invitation(author_id=user.id)
    session.add(invitation)
    session.commit()
    return invitation


@router.post('/{invite_token}', status_code=201, response_model=UserSchema)
def create_invite_user(user: UserCreateSchema, invite_token: str, session=Depends(get_db)):
    invite = Invitation.get_from_token(invite_token, session=session)
    if not invite:
        raise InvalidRequest('Invalid Token')
    user = create_user(user)
    invite.consumer = user
    return user
