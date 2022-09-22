from app import Blueprint, auth, db
from app.db.models import Hospital

bp = Blueprint(__name__)


@bp.get('/')
@auth.check()
def get_hospitals(name: str = None, city_id: int = None):
    query = db.session.query(Hospital)
    if name:
        query = query.filter(Hospital.name.ilike(f'%{name}%'))
    if city_id:
        query = query.filter_by(city_id=city_id)
    return query


@bp.get('/<int:hospital_id>')
@auth.check()
def get_hospital(hospital_id: int):
    return db.get(Hospital, hospital_id, error_on_unfound=True)
