from datetime import date
from typing import Optional
from app import db
from app.models import heart


class HeartSchema(db.Schema):
    listing_id: Optional[int]

    listing_id: int
    score: Optional[float]
    R_D_NAI: Optional[date]
    D_INSC: Optional[date]
    tailler: Optional[float]
    poidsr: Optional[float]
    urgence: Optional[heart.HeartScore.URGENCE]
    d_urgence: Optional[date]
    KXPC: Optional[str]
    XPC: Optional[str]
    DRG: Optional[bool]
    CEC: Optional[bool]
    DCEC: Optional[date]
    SIAV: Optional[str]
    CAT: Optional[str]
    BNP: Optional[int]
    DBNP: Optional[int]
    PROBNP: Optional[float]
    DPROBNP: Optional[date]

    score: Optional[int]

    class Config:
        orm_mode = True


class HeartCreateSchema(HeartSchema):
    listing_id: int
    score: Optional[float]
    R_D_NAI: Optional[date]
    D_INSC: Optional[date]
    tailler: Optional[float]
    poidsr: Optional[float]
    urgence: Optional[heart.HeartScore.URGENCE]
    d_urgence: Optional[date]
    KXPC: Optional[str]
    XPC: Optional[str]
    DRG: Optional[bool]
    CEC: Optional[bool]
    DCEC: Optional[date]
    SIAV: Optional[str]
    CAT: Optional[str]
    BNP: Optional[int]
    DBNP: Optional[int]
    PROBNP: Optional[float]
    DPROBNP: Optional[date]

    score: Optional[int]


class HeartUpdateSchema(HeartSchema):
    listing_id: int
    R_D_NAI: Optional[date]
    D_INSC: Optional[date]
    tailler: Optional[float]
    poidsr: Optional[float]
    urgence: Optional[heart.HeartScore.URGENCE]
    d_urgence: Optional[date]
    KXPC: Optional[str]
    XPC: Optional[str]
    DRG: Optional[bool]
    CEC: Optional[bool]
    DCEC: Optional[date]
    SIAV: Optional[str]
    CAT: Optional[str]
    BNP: Optional[int]
    DBNP: Optional[int]
    PROBNP: Optional[float]
    DPROBNP: Optional[date]


class HeartUpdateScore(HeartSchema):
    score: float
