from app import db
from .city import CitySchema


class HospitalSchema(db.Schema):
    city: CitySchema
    name: str

    class Config:
        orm_mode = True
