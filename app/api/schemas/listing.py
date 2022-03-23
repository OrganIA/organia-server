from datetime import date
from optparse import Option
from typing import Optional
from app import db
from app.models import Listing
from app.api.schemas.person import PersonGetSchema


class ListingSchema(db.Schema):
    start_date: Optional[date]
    end_date: Optional[date]
    notes: Optional[str]
    organ: Listing.Organ
    donor: bool
    tumors_number: int
    biggest_tumor_size: Optional[int]
    alpha_fetoprotein: Optional[int]
    isDialyse: bool
    isRetransplantation: bool
    startDateDialyse: Optional[date]
    EndDateDialyse: Optional[date]
    ARFDate: Optional[date]
    DateTransplantation: Optional[date]
    ReRegistrationDate: Optional[date]
    A: Optional[int]
    B: Optional[int]
    DR: Optional[int]
    DQ: Optional[int]

    class Config:
        orm_mode = True


class ListingUpdateSchema(ListingSchema):
    organ: Optional[Listing.Organ]
    donor: Optional[bool]
    tumors_number: Optional[int]
    biggest_tumor_size: Optional[int]
    alpha_fetoprotein: Optional[int]
    person_id: Optional[int]


class ListingCreateSchema(ListingSchema):
    person_id: int


class ListingGetSchema(ListingSchema):
    person: PersonGetSchema
