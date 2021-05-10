from fastapi import APIRouter

router = APIRouter(prefix='/users')


# TODO dummy
@router.get('/')
async def users():
    return [{'name': 'bob'} for _ in range(10)]

from . import models
