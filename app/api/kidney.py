from fastapi import APIRouter
from typing import List
from app.api.persons import get_person

from app import db
from app.errors import NotFoundError, InvalidRequest
from app.models import Kidney, Listing
from app.api.schemas.kidney import (
    KidneySchema, KidneyUpdateScore
)
from score.Kidney.KidneyScore import getScoreNAP

router = APIRouter(prefix='/kidneys')


@router.get('/{listing_id}', response_model=KidneySchema)
async def get_kidneys(listing_id: int):
    query = db.session.query(Kidney).filter_by(listing_id=listing_id).first()
    if not query:
        raise NotFoundError('No Listing found')
    return query


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


@router.post('/{listing_id}/score', status_code=201, response_model=KidneySchema)
async def update_kidney_score(listing_id: int, score: KidneyUpdateScore):
    listing = db.session.query(Listing).filter_by(id=listing_id).first()
    if listing == None:
        raise NotFoundError('Listing not found')
    kidney = await get_kidneys(listing_id)
    kidney.score = score.score
    db.session.commit()
    return kidney


@router.get('/{listing_id}/score_del', status_code=201)
async def delete_kidney_score(listing_id: int):
    listing = db.session.query(Listing).filter_by(id=listing_id).first()
    if listing == None:
        raise NotFoundError('listing_id', listing_id,
                            'doesn\'t refer to an existing listing')
    kidney = await get_kidneys(listing_id)
    kidney.score = 0.0
    db.session.commit()
    return kidney


@router.get('/{listing_id}/matches', status_code=201)
async def compute_matches(listing_id: int):
    receivers_listings = db.session.query(Listing).filter_by(
        Listing.id != listing_id, Listing.donor == False, Listing.organ == "KIDNEY").all()
    donor_listing = db.session.query(Listing).filter_by(
        Listing.id == listing_id).first()
    donor_person = await get_person(listing_id)
    listings_ids = []
    for receiver in receivers_listings:
        listings_ids.append(receiver.id)
        listing_person = await get_person(receiver.person_id)
        getScoreNAP(listing_person, donor_person, receiver)
    return
