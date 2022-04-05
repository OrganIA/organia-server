from app import db
from typing import Optional



class HospitalSchema(db.Schema):
    city_id: int
    name: str
    latitude: Optional[float]
    longitude: Optional[float]
    patient_number: Optional[int]

    class Config:
        orm_mode = True


class HospitalGetSchema(HospitalSchema, db.TimedMixin.Schema):
    latitude: Optional[float]
    longitude: Optional[float]

class HospitalUpdateSchema(HospitalSchema):
    name: Optional[str]
    patient_number: Optional[int]