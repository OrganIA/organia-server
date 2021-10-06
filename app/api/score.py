from typing import List
from fastapi import APIRouter

from app import db
from app.errors import NotFoundError
from app.models import Person
from app.api.schemas.person import (
    PersonSchema, PersonGetSchema, PersonUpdateSchema,
)
from .dependencies import logged_user


router = APIRouter(prefix='/score') # Do not forget to add permissions


@router.get('/{listing_id}')
async def get_receivers_from_donor():
    return db.session.query(Person).all()
