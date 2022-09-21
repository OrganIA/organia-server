from datetime import date
from typing import Optional
from app import db
from app.models import Listing
from app.api.schemas.person import PersonGetSchema


class ListingSchema(db.Schema):
    start_date: Optional[date]
    end_date: Optional[date]
    hospital_id: Optional[int]
    notes: Optional[str]
    organ: Listing.Organ
    donor: bool
    tumors_number: Optional[int]
    biggest_tumor_size: Optional[int]
    alpha_fetoprotein: Optional[int]
    A: Optional[int]
    B: Optional[int]
    DR: Optional[int]
    DQ: Optional[int]

    body_mass_index: Optional[float]
    diabetes: Optional[bool]
    functional_status_assistance_required: Optional[bool]
    FVC_percentage: Optional[float]
    PA_systolic: Optional[float]
    oxygen_requirement: Optional[float]
    six_minute_walk_distance_over_150_feet: Optional[bool]
    continuous_mechanical_ventilation: Optional[bool]
    PC02: Optional[float]
    PCO2_increase_superior_to_15_percent: Optional[bool]
    diagnosis_group: Optional[str]
    detailled_diagnosis: Optional[str]

    age_at_transplant: Optional[int]
    creatinine_at_transplant: Optional[float]
    ADL_required: Optional[bool]
    PCW_over_20_mmHg: Optional[bool]

    class Config:
        orm_mode = True


class ListingUpdateSchema(ListingSchema):
    organ: Optional[Listing.Organ]
    donor: Optional[bool]
    tumors_number: Optional[int]
    biggest_tumor_size: Optional[int]
    alpha_fetoprotein: Optional[int]
    person_id: Optional[int]
    hospital_id: Optional[int]



class ListingCreateSchema(ListingSchema):
    person_id: int


class ListingGetSchema(ListingSchema, Listing.Schema):
    person: PersonGetSchema
