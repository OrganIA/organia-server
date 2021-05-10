from app.db import session
from . import router
from .models import User


@router.get('/')
async def users():
    return [x.name for x in session.query(User).all()]
