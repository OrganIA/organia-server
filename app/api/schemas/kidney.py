from datetime import date
from optparse import Option
from tokenize import String
from typing import Optional
from app import db
from app.models import kidney


class KidneySchema(db.Schema):
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
        
class KidneyUpdateScore(db.Schema):
    score: float
    
    class Config:
        orm_mode = True