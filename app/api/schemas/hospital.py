from app import db

class HospitalSchema(db.Schema):
    department: int
    city: str
    name: str