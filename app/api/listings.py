from typing import List
from fastapi import APIRouter

from app import db
from app.errors import NotFoundError, InvalidRequest
from app.models import Listing
from app.api.schemas.listing import (
    ListingGetSchema, ListingCreateSchema, ListingUpdateSchema,
)


router = APIRouter(prefix='/listings')


@router.get('/organs')
async def get_organs():
    return Listing.Organ.values()


@router.get('/', response_model=List[ListingGetSchema])
async def get_listings():
    return db.session.query(Listing).all()


@router.get('/donors', response_model=List[ListingGetSchema])
async def get_donors():
    return db.session.query(Listing).filter(Listing.donor).all()


@router.get('/receivers', response_model=List[ListingGetSchema])
async def get_receivers():
    return db.session.query(Listing).filter(~Listing.donor).all()


@router.post('/', response_model=ListingGetSchema)
async def create_listing(data: ListingCreateSchema):
    listing = Listing.from_data(data)
    db.session.add(listing)
    db.session.commit()
    return listing


@router.get('/{listing_id}', response_model=ListingGetSchema)
async def get_listing(listing_id):
    return db.session.get(Listing, listing_id) or NotFoundError.r()


@router.post('/{listing_id}', response_model=ListingGetSchema)
async def update_listing(listing_id, data: ListingUpdateSchema):
    listing = await get_listing(listing_id)
    listing.update(data)
    if listing.person is None:
        db.session.rollback()
        raise InvalidRequest('Could not find a corresponding person')
    db.session.commit()
    return listing


@router.delete('/{listing_id}')
async def delete_listing(listing_id: int):
    listing = await get_listing(listing_id)
    db.session.delete(listing)
    db.session.commit()
