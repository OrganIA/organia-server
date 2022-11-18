from fastapi import APIRouter

from app import db
from app.errors import NotFoundError, InvalidRequest
from app.models import Lung, Listing
from app.api.schemas.lung import (
    LungSchema, LungCreateSchema
)
from app.api.persons import get_person
from app.score.Lungs.LungsScore import lungs_final_score

router = APIRouter(prefix='/lungs')


@router.get('/{listing_id}', response_model=LungSchema)
async def get_lungs(listing_id: int):
    query = db.session.query(Lung).filter_by(listing_id=listing_id).first()
    if not query:
        raise NotFoundError('No Listing found')
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
async def update_lungs_score(listing_id: int, score: float):
    listing = db.session.query(Listing).filter_by(id=listing_id).first()
    if listing == None:
        raise NotFoundError('Listing not found')
    lung = await get_lungs(listing_id)
    lung.score = score
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


@router.get('/{listing_id}/matches', status_code=201)
async def compute_matches(listing_id: int):
    listing_lungs_receivers = db.session.query(Listing).filter(
        Listing.id != listing_id, Listing.donor == False, Listing.organ == "LUNG").all()
    listing_lungs_receiver_ids = []
    for listing_lungs_receiver in listing_lungs_receivers:
        listing_lungs_receiver_ids.append(listing_lungs_receiver.id)
        person_receiver = await get_person(listing_lungs_receiver.person_id)
        await update_lungs_score(listing_lungs_receiver.id, lungs_final_score(person_receiver, None, listing_lungs_receiver))
    return db.session.query(Lung).filter(Lung.listing_id.in_(listing_lungs_receiver_ids)).order_by(Lung.score.desc()).all()
