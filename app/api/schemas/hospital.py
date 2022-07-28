from typing import Optional

from app import db
from .city import CitySchema


class HospitalSchema(db.Schema):
    city: CitySchema
    name: str
    phone_number: Optional[str]

    class Config:
        orm_mode = True


class HospitalGetSchema(HospitalSchema, db.TimedMixin.Schema):
    latitude: Optional[float]
    longitude: Optional[float]
    patients_count: Optional[int]

class HospitalUpdateSchema(HospitalSchema):
    name: Optional[str]
    phone_number: Optional[str]
