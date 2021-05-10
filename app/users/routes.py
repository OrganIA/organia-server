from typing import List

from app.db import session
from app.models import User, UserSchema
from . import router


@router.get('/', response_model=List[UserSchema])
async def users():
    return session.query(User).all()
