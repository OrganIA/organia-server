from fastapi import APIRouter

from app import db
from app.errors import NotFoundError, InvalidRequest
from app.models import Liver, Listing
from app.api.schemas.liver import (
    LiverCreateSchema, LiverSchema, LiverUpdateScore,
)
from app.score.Liver.LiverScore import final_score
from app.api.persons import get_person
router = APIRouter(prefix='/livers')


@router.get('/{listing_id}', response_model=LiverSchema)
async def get_livers(listing_id: int):
    query = db.session.query(Liver).filter_by(listing_id=listing_id).first()
    if not query:
        raise NotFoundError.r('No Listing found')
    return query

@router.post('/{listing_id}', status_code=201, response_model=LiverSchema)
async def update_livers_variables(listing_id: int, data: LiverCreateSchema):
    listing = db.session.query(Listing).filter_by(id=listing_id).first()
    if listing == None:
        raise NotFoundError.r('Listing not found')
    listing_lung = db.session.query(Liver).filter_by(
        listing_id=listing_id).first()
    if listing_lung != None:
        raise NotFoundError.r('A listing with this id already exists')
    data.listing_id = listing_id
    data = data.dict(exclude_unset=True)
    livers = db.add(Liver, data)
    return livers

@router.get('/{listing_id}/matches')
async def match_liver(listing_id):
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
            receiver = await get_person(listing_receiver.person_id)
            score = final_score(receiver, donor, listing_receiver, listing_donor)
            list_score.append({"listing_id": listing_receiver.id, "score": score})
        return sorted(list_score, key=lambda d: d["score"], reverse=True)

@router.post('/{listing_id}/score', status_code=201, response_model=LiverSchema)
async def update_livers_score(listing_id: int, score: LiverUpdateScore):
    listing = db.session.query(Listing).filter_by(id=listing_id).first()
    if listing == None:
        raise NotFoundError.r('Listing not found')
    liver = await get_livers(listing_id)
    liver.score = score.score
    db.session.commit()
    return liver

@router.delete('/{listing_id}/score_del', status_code=201)
async def delete_livers_score(listing_id: int):
    listing = db.session.query(Listing).filter_by(id=listing_id).first()
    if listing == None:
        raise NotFoundError.r('listing_id', listing_id,
                            'doesn\'t refer to an existing listing')
    liver = await get_livers(listing_id)
    liver.score = 0.0
    db.session.commit()
