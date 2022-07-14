from typing import List
from fastapi import APIRouter

from app import db
from app.errors import NotFoundError, InvalidRequest
from app.models import Liver, Listing
from app.api.schemas.liver import (
    LiverGetSchema, LiverCreateSchema, LiverSchema, LiverUpdateSchema,
)

router = APIRouter(prefix='/livers')

@router.get('/{listing_id}}', response_model=List[LiverSchema])
async def get_livers(listing_id: int):
    query = db.session.query(Liver).filter_by(listing_id=listing_id).first()
    return query
