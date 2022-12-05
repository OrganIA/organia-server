from datetime import datetime

from app import db
from app.db.models import Heart
from app.errors import NotFoundError
from app.utils.bp import Blueprint
from app.utils.static import Static

bp = Blueprint(__name__)


class HeartSchema(Static):
    @staticmethod
    def R_D_NAI(d):
        R_D_NAI = Static._get(d, 'R_D_NAI')
        return datetime.fromisoformat(R_D_NAI).date()

    @staticmethod
    def D_INSC(d):
        D_INSC = Static._get(d, 'D_INSC')
        return datetime.fromisoformat(D_INSC).date()

    @staticmethod
    def d_urgence(d):
        d_urgence = Static._get(d, 'd_urgence')
        return datetime.fromisoformat(d_urgence).date()

    @staticmethod
    def DCEC(d):
        DCEC = Static._get(d, 'DCEC')
        return datetime.fromisoformat(DCEC).date()

    @staticmethod
    def DPROBNP(d):
        DPROBNP = Static._get(d, 'd_urgence')
        return datetime.fromisoformat(DPROBNP).date()

    @staticmethod
    def DCREAT(d):
        DCREAT = Static._get(d, 'DCREAT')
        return datetime.fromisoformat(DCREAT).date()

    @staticmethod
    def DBILI(d):
        DBILI = Static._get(d, 'DBILI')
        return datetime.fromisoformat(DBILI).date()

    @staticmethod
    def D_D_NAI(d):
        D_D_NAI = Static._get(d, 'D_D_NAI')
        return datetime.fromisoformat(D_D_NAI).date()

    @staticmethod
    def D_PREL(d):
        D_PREL = Static._get(d, 'D_PREL')
        return datetime.fromisoformat(D_PREL).date()

    @staticmethod
    def urgence(d):
        urgence = Static._get(d, 'urgence')
        return datetime.fromisoformat(urgence).date()

    ABO_D = str
    sex_D = str
    MAL = str
    MAL2 = str
    MAL3 = str
    # urgence
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
