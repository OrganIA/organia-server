from fastapi import APIRouter
from typing import List

from app import db
from app.errors import NotFoundError, InvalidRequest
from app.models import HeartScore, Listing
from app.api.schemas.heart import (
    HeartSchema, HeartCreateSchema, HeartUpdateSchema, HeartUpdateScore
)

router = APIRouter(prefix='/heart')


@router.get('/{listing_id}', response_model=HeartSchema)
async def get_heart(listing_id: int):
    query = db.session.query(HeartScore).filter_by(
        listing_id=listing_id).first()
    if not query:
        raise NotFoundError('No Listing found')
    return query


@router.post('/{listing_id}', status_code=201, response_model=HeartSchema)
async def create_heart_variables(listing_id: int, data: HeartCreateSchema):
    listing = db.session.query(Listing).filter_by(id=listing_id).first()
    if listing == None:
        raise NotFoundError('Listing not found')
    listing_heart = db.session.query(HeartScore).filter_by(
        listing_id=listing_id).first()
    if listing_heart != None:
        raise InvalidRequest('A listing with this id already exists')

    data.listing_id = listing_id
    data = data.dict(exclude_unset=True)
    heart = db.add(HeartScore, data)
    return heart


@router.put('/{listing_id}', status_code=201, response_model=HeartSchema)
async def update_heart_score(listing_id: int, data: HeartUpdateSchema):
    listing = db.session.query(Listing).filter_by(id=listing_id).first()
    if listing == None:
        raise NotFoundError('Listing not found')
    heart = await get_heart(listing_id)
    heart.update(data)
    db.session.commit()
    return heart


@router.put('/{listing_id}/score', status_code=201, response_model=HeartSchema)
async def update_heart_score(listing_id: int, score: HeartUpdateScore):
    listing = db.session.query(Listing).filter_by(id=listing_id).first()
    if listing == None:
        raise NotFoundError('Listing not found')
    heart = await get_heart(listing_id)
    heart.score = score.score
    db.session.commit()
    return heart


@router.delete('/{listing_id}', status_code=201)
async def delete_heart_score(listing_id: int):
    listing = db.session.query(Listing).filter_by(id=listing_id).first()
    if listing == None:
        raise NotFoundError('listing_id', listing_id,
                            'doesn\'t refer to an existing listing')
    heart = await get_heart(listing_id)
    heart.score = 0.0
    db.session.commit()
    return
