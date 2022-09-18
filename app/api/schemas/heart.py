from datetime import date
from optparse import Option
from tokenize import String
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
    MAL: Optional[heart.HeartScore.MAL]
    MAL2: Optional[heart.HeartScore.MAL]
    MAL3: Optional[heart.HeartScore.MAL]
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
    MAL: Optional[heart.HeartScore.MAL]
    MAL2: Optional[heart.HeartScore.MAL]
    MAL3: Optional[heart.HeartScore.MAL]
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
    MAL: Optional[heart.HeartScore.MAL]
    MAL2: Optional[heart.HeartScore.MAL]
    MAL3: Optional[heart.HeartScore.MAL]
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
