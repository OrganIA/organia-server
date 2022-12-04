from app import db
from app.db.models import Heart
from app.errors import NotFoundError
from app.utils.bp import Blueprint
from app.utils.static import Static

bp = Blueprint(__name__)


class HeartSchema(Static):
    listing_id = int
    taille_D = float
    poids_D = float
    ABO_D = str
    sex_D = str
    R_D_NAI = date
    D_INSC = date
    MAL = str
    MAL2 = str
    MAL3 = str


@bp.get('/')
def get_livers():
    return db.session.query(Heart)


@bp.get('/<int:id>')
def get_heart(id):
    result = db.session.get(Heart, id)
    if not result:
        raise NotFoundError
    return result


# @bp.post('/')
# def create_heart(data: LiverSchema):
#     heart = Heart(**data.dict)
#     db.session.add(heart)
#     db.session.commit()
#     return get_heart(heart.id)


@bp.delete('/<int:id>')
def delete_heart(id: int):
    heart = get_heart(id)
    db.session.delete(heart)
    db.session.commit()
