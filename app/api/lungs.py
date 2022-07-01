from fastapi import APIRouter
from api.schemas.listing import ListingGetSchema
from typing import List

from app import db
from app.errors import NotFoundError, InvalidRequest
from app.models import Lung, Listing
from app.api.schemas.lung import (
    LungSchema, LungCreateSchema
)

router = APIRouter(prefix='/lungs')


@router.get('/{listing_id}', response_model=List[LungSchema])
async def get_lungs(listing_id: int):
    query = db.session.query(Lung).filter_by(listing_id=listing_id).first()
    return query


@router.post('/{listing_id}', status_code=201)
async def update_lungs_variables(listing_id: int, data: LungCreateSchema):
    listing = db.session.query(Listing).filter_by(id=listing_id).first()
    if listing == None:
        raise NotFoundError('listing_id', listing_id,
                            'doesn\'t refer to an existing listing')
    listing_lung = db.session.query(Lung).filter_by(
        listing_id=listing_id).first()
    if listing_lung != None:
        raise InvalidRequest('A listing with this id already exists')
    column_list = []
    for column_name in Lung.__table__.columns.keys():
        column_list.append(column_name)
    for property in data:
        if property[0] not in column_list:
            raise InvalidRequest(property[0], 'is not a valid property')
    data.listing_id = listing_id
    data = data.dict(exclude_unset=True)
    db.add(Lung, data)
    return


@router.post('/{listing_id}/score', status_code=201)
async def update_lungs_score(listing_id: int, score: int):
    listing = db.session.query(Listing).filter_by(id=listing_id).first()
    if listing == None:
        raise NotFoundError('listing_id', listing_id,
                            'doesn\'t refer to an existing listing')
    if type(score) is not float:
        raise InvalidRequest('score should be of type float')
    lung = await get_lungs(listing_id)
    lung.score = score
    db.session.commit()
    return
