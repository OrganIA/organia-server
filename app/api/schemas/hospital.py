from app import db

class HospitalSchema(db.Schema):
    city_id: int
    name: str

class City(db.Schema):
    name: str
    department_code: str