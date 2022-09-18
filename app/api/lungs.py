from fastapi import APIRouter
from typing import List

from app import db
from app.errors import NotFoundError, InvalidRequest
from app.models import Lung, Listing
from app.api.schemas.lung import (
    LungSchema, LungCreateSchema, LungUpdateScore
)

router = APIRouter(prefix='/lungs')


@router.get('/{listing_id}', response_model=LungSchema)
async def get_lungs(listing_id: int):
    query = db.session.query(Lung).filter_by(listing_id=listing_id).first()
    return query


@router.post('/{listing_id}', status_code=201, response_model=LungSchema)
async def update_lungs_variables(listing_id: int, data: LungCreateSchema):
    listing = db.session.query(Listing).filter_by(id=listing_id).first()
    if listing == None:
        raise NotFoundError('Listing not found')
    listing_lung = db.session.query(Lung).filter_by(
        listing_id=listing_id).first()
    if listing_lung != None:
        raise InvalidRequest('A listing with this id already exists')

    data.listing_id = listing_id
    data = data.dict(exclude_unset=True)
    lungs = db.add(Lung, data)
    return lungs


@router.post('/{listing_id}/score', status_code=201, response_model=LungSchema)
async def update_lungs_score(listing_id: int, score: LungUpdateScore):
    listing = db.session.query(Listing).filter_by(id=listing_id).first()
    if listing == None:
        raise NotFoundError('Listing not found')
    lung = await get_lungs(listing_id)
    lung.score = score.score
    db.session.commit()
    return lung


@router.get('/{listing_id}/score_del', status_code=201)
async def delete_lungs_score(listing_id: int):
    listing = db.session.query(Listing).filter_by(id=listing_id).first()
    if listing == None:
        raise NotFoundError('listing_id', listing_id,
                            'doesn\'t refer to an existing listing')
    lung = await get_lungs(listing_id)
    lung.score = 0.0
    db.session.commit()
    return
