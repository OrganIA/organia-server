from datetime import date
from typing import Optional
from app import db
from app.models import Kidney


class KidneySchema(db.TimedMixin.Schema):
    listing_id: Optional[int]

    isDialyse: Optional[bool]
    isRetransplantation: Optional[bool]
    startDateDialyse: Optional[date]
    EndDateDialyse: Optional[date]
    ARFDate: Optional[date]
    DateTransplantation: Optional[date]
    ReRegistrationDate: Optional[date]

    score: Optional[int]

    class Config:
        orm_mode = True


class KidneyCreateSchema(KidneySchema):
    id: Optional[int]
    listing_id: Optional[int]

    isDialyse: Optional[bool]
    isRetransplantation: Optional[bool]
    startDateDialyse: Optional[date]
    EndDateDialyse: Optional[date]
    ARFDate: Optional[date]
    DateTransplantation: Optional[date]
    ReRegistrationDate: Optional[date]

    class Config:
        orm_mode = True


class KidneyUpdateScore(db.Schema):
    score: float

    class Config:
        orm_mode = True
