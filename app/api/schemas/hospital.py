from typing import Optional

from app import db
from app.models import Hospital

class HospitalSchema(db.Schema):
    department: int
    city: str
    h_name: str