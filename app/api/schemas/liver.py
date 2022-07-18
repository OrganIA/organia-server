from datetime import date
from optparse import Option
from tokenize import String
from typing import Optional
from app import db
from app.models import liver
from app.api.schemas.listing import ListingGetSchema


class LiverSchema(db.Schema):
    listing_id: Optional[int]
    tumors_number: Optional[int]
    biggest_tumor_size: Optional[int]
    alpha_fetoprotein: Optional[int]

    score: Optional[int]

    class Config:
        orm_mode = True

class LiverUpdateSchema(db.Schema):
    listing_id: Optional[int]
    tumors_number: int
    biggest_tumor_size: Optional[int]
    alpha_fetoprotein: Optional[int]
    
class LiverCreateSchema(LiverSchema):
    listing_id: Optional[int]

class LiverGetSchema(LiverSchema):
    listing: ListingGetSchema

class LiverUpdateScore(db.Schema):
    score: float
