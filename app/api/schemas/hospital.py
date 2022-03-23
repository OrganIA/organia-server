from app import db


class HospitalSchema(db.Schema):
    city_id: int
    name: str

    class Config:
        orm_mode = True
