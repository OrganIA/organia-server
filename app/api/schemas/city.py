from app import db


class CitySchema(db.Schema):
    name: str
    department_code: str

    class Config:
        orm_mode = True
