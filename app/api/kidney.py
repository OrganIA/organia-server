from fastapi import APIRouter
from typing import List

from app import db
from app.errors import NotFoundError, InvalidRequest
from app.models import Kidney, Listing
from app.api.schemas.kidney import (
    KidneySchema, KidneyUpdateScore
)

router = APIRouter(prefix='/kidneys')

@router.post('/{listing_id}', status_code=201, response_model=KidneySchema)
async def create_kidney_variables(listing_id: int, data: KidneySchema):
    listing = db.session.query(Listing).filter_by(id=listing_id).first()
    if listing == None:
        raise NotFoundError('Listing not found')
    listing_kidney = db.session.query(Kidney).filter_by(
        listing_id=listing_id).first()
    if listing_kidney != None:
        raise InvalidRequest('A listing with this id already exists')

    data.listing_id = listing_id
    data = data.dict(exclude_unset=True)
    kidney = db.add(Kidney, data)
    return kidney