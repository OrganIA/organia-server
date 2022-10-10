from typing import List
from fastapi import APIRouter

from app import db
from app.errors import NotFoundError, InvalidRequest
from app.models import Liver, Listing
from app.api.schemas.liver import (
    LiverCreateSchema, LiverSchema, LiverUpdateScore,
)

router = APIRouter(prefix='/livers')


@router.get('/{listing_id}', response_model=LiverSchema)
async def get_livers(listing_id: int):
    query = db.session.query(Liver).filter_by(listing_id=listing_id).first()
    if not query:
        raise NotFoundError('No Listing found')
    return query

@router.post('/{listing_id}', status_code=201, response_model=LiverSchema)
async def update_livers_variables(listing_id: int, data: LiverCreateSchema):
    listing = db.session.query(Listing).filter_by(id=listing_id).first()
    if listing == None:
        raise NotFoundError('Listing not found')
    listing_lung = db.session.query(Liver).filter_by(
        listing_id=listing_id).first()
    if listing_lung != None:
        raise InvalidRequest('A listing with this id already exists')

    data.listing_id = listing_id
    data = data.dict(exclude_unset=True)
    livers = db.add(Liver, data)
    return livers

@router.post('/{listing_id}/score', status_code=201, response_model=LiverSchema)
async def update_livers_score(listing_id: int, score: LiverUpdateScore):
    listing = db.session.query(Listing).filter_by(id=listing_id).first()
    if listing == None:
        raise NotFoundError('Listing not found')
    liver = await get_livers(listing_id)
    liver.score = score.score
    db.session.commit()
    return liver

@router.delete('/{listing_id}/score_del', status_code=201)
async def delete_livers_score(listing_id: int):
    listing = db.session.query(Listing).filter_by(id=listing_id).first()
    if listing == None:
        raise NotFoundError('listing_id', listing_id,
                            'doesn\'t refer to an existing listing')
    liver = await get_livers(listing_id)
    liver.score = 0.0
    db.session.commit()
    return