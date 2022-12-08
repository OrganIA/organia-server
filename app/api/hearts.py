from datetime import date

from pydantic import BaseModel

from app import db
from app.db.models import Heart
from app.errors import NotFoundError
from app.utils.bp import Blueprint

bp = Blueprint(__name__)


class HeartSchema(BaseModel):
    DPROBNP: date | None
    DCREAT: date | None
    DBILI: date | None
    urgence: date | None
    ABO_D: str | None
    sex_D: str | None
    MAL: str | None
    MAL2: str | None
    MAL3: str | None
    KXPC: str | None
    XPC: int | None
    DRG: str | None
    CEC: str | None
    SIAV: str | None
    CAT: str | None
    BNP: int | None
    DBNP: int | None
    PROBNP: float | None
    DIA: str | None
    DCREAT: date | None
    CREAT: float | None
    BILI: float | None
    BNP_AVI: float | None
    PBN_AVI: float | None
    DIA_AVI: str | None
    CRE_AVI: float | None
    BILI_AVI: float | None
    TTLGP: float | None
    ICAR: float | None
    F_ICAR: float | None
    delai_var_bio_GRF: date | None
    date_courante: date | None


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
    heart = Heart(**data.dict())
    return heart
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
