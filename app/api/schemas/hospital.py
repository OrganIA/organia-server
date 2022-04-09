from app import db
from typing import Optional


class HospitalSchema(db.Schema):
    city_id: int
    name: str
    phone_number: Optional[str]

    class Config:
        orm_mode = True


class HospitalGetSchema(HospitalSchema, db.TimedMixin.Schema):
    latitude: Optional[float]
    longitude: Optional[float]
    patient_number: Optional[int]

class HospitalUpdateSchema(HospitalSchema):
    name: Optional[str]
    phone_number: Optional[str]
    patient_number: Optional[int]
