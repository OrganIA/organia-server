from app import db


class City(db.Schema):
    name: str
    department_code: str
