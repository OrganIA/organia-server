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
    dialyse: bool
    retransplantation: bool
    start_date_dialyse: Optional[date]
    end_date_dialyse: Optional[date]
    arf_date: Optional[date]
    transplantation_date: Optional[date]
    second_registration_date: Optional[date]
    hla: Listing.HLA

    class Config:
        orm_mode = True


class ListingUpdateSchema(ListingSchema):
    organ: Optional[Listing.Organ]
    donor: Optional[bool]
    person_id: Optional[int]
    hla: Optional[Listing.HLA]


class ListingCreateSchema(ListingSchema):
    person_id: int


class ListingGetSchema(ListingSchema):
    person: PersonGetSchema
