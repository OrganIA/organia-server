from datetime import date

from pydantic import BaseModel

from app import db
from app.db.models import Heart
from app.errors import NotFoundError
from app.utils.bp import Blueprint

bp = Blueprint(__name__)


class HeartSchema(BaseModel):
    R_D_NAI = date
    D_INSC = date
    d_urgence = date
    DCEC = date
    DPROBNP = date
    DCREAT = date
    DBILI = date
    D_D_NAI = date
    D_PREL = date
    urgence = date
    ABO_D = str
    sex_D = str
    MAL = str
    MAL2 = str
    MAL3 = str
    KXPC = str
    XPC = int
    DRG = str
    CEC = str
    SIAV = str
    CAT = str
    BNP = int
    DBNP = int
    PROBNP = float
    DIA = str
    CREAT = float
    BILI = float
    BNP_AVI = float
    PBN_AVI = float
    DIA_AVI = str
    CRE_AVI = float
    BILI_AVI = float
    TTLGP = float
    ICAR = float
    F_ICAR = float
    comp_ad_std = float
    comp_ad_XPCA = float
    comp_ped_std = float
    comp_ped_XPCP = float
    score_CCN = float
    F1_dif_age = bool
    F2_ABO = bool
    F3_SC = bool
    F4_surv_post_GRF = bool
    score_CCP = float
    score_NACG = float
    score = float


def update(listing, data):
    for key, value in data.dict.items():
        if value == 'null':
            setattr(listing, key, None)
        elif value is not None:
            setattr(listing, key, value)
    return listing


@bp.get('/')
def get_livers():
    return db.session.query(Heart)


@bp.get('/<int:id>')
def get_heart(id):
    result = db.session.get(Heart, id)
    if not result:
        raise NotFoundError
    return result


@bp.post('/')
def create_heart(data: HeartSchema):
    heart = Heart(**data.dict)
    db.session.add(heart)
    db.session.commit()
    return get_heart(heart.id)


@bp.post('/<int:id>')
def update_heart(id, data):
    heart = db.session.get(Heart, id)
    if not heart:
        raise NotFoundError
    heart = update(heart, data)
    db.session.commit()
    return heart


@bp.delete('/<int:id>')
def delete_heart(id: int):
    heart = get_heart(id)
    db.session.delete(heart)
    db.session.commit()
