from app import db
from app.db.models import Liver
from app.errors import NotFoundError
from app.utils.bp import Blueprint
from app.utils.static import Static

bp = Blueprint(__name__)


class LiverSchema(Static):
    listing_id = int
    tumors_number = int
    biggest_tumor_size = int
    alpha_fetoprotein = int
    score = int


@bp.get('/')
def get_livers():
    return db.session.query(Liver)


@bp.get('/<int:id>')
def get_liver(id):
    result = db.session.get(Liver, id)
    if not result:
        raise NotFoundError
    return result


@bp.post('/')
def create_liver(data: LiverSchema):
    liver = Liver(**data.dict)
    db.session.add(liver)
    db.session.commit()
    return get_liver(liver.id)


@bp.delete('/<int:id>')
def delete_liver(id: int):
    liver = get_liver(id)
    db.session.delete(liver)
    db.session.commit()
