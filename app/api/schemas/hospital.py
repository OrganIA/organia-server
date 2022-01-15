from app import db
from .city import CitySchema


class HospitalSchema(db.Schema):
    city_id: int
    name: str

    class Config:
        orm_mode = True