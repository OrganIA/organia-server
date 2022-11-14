from fastapi import APIRouter
from typing import List

from app import db
from app.errors import NotFoundError, InvalidRequest
from app.models import HeartScore, Listing
from app.api.schemas.heart import (
    HeartSchema, HeartCreateSchema, HeartUpdateSchema, HeartUpdateScore
)

from app.api.persons import get_person

router = APIRouter(prefix='/hearts')


@router.get('/', response_model=List[HeartSchema])
async def get_hearts():
    return db.session.query(HeartScore).all()

@router.get('/{listing_id}', response_model=HeartSchema)
async def get_heart(listing_id: int):
    query = db.session.query(HeartScore).filter_by(
        listing_id=listing_id).first()
    if not query:
        raise NotFoundError('No Listing found')
    return query


@router.post('/', status_code=201, response_model=HeartSchema)
async def create_heart_variables(data: HeartCreateSchema):
    listing_id = data.listing_id
    listing = db.session.query(Listing).filter_by(id=listing_id).first()
    if listing == None:
        raise NotFoundError('Listing not found')
    listing_heart = db.session.query(HeartScore).filter_by(
        listing_id=listing_id).first()
    if listing_heart != None:
        raise InvalidRequest('A listing with this id already exists')
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


@router.get('/{listing_id}/matches')
async def match_heart(listing_id):
    list_score = []
    listing_donor = db.session.get(Listing, listing_id)
    if listing_donor.donor is False:
        return InvalidRequest.r("This patient is not a donor")
    donor = await get_person(listing_donor.person_id)
    listings = db.session.query(Listing).filter(~Listing.donor).all()
    if listings is None:
        return NotFoundError.r("List is empty: ", listings)
    else:
        for listing_receiver in listings:
            if listing_receiver.organ.value == "HEART":
                heart_receiver = await get_heart(listing_receiver.id)
                score = heart_receiver.getICAR()
                print(score)
                list_score.append({"listing_id": listing_receiver.id, "score": score})
            else:
                continue
    return sorted(list_score, key=lambda d: d["score"], reverse=True)
