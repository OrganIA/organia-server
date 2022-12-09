from pydantic import BaseModel

from app import db, geopy
from app.db.models import City, Hospital
from app.errors import NotFoundError
from app.utils.bp import Blueprint

bp = Blueprint(__name__)


class HospitalSchema(BaseModel):
    name: str
    phone_number: str | None
    latitude: float | None
    longitude: float | None
    city_id: int | None


def create_city(city_data):
    obj = (
        db.session.query(City)
        .filter_by(department_code=city_data["department_code"])
        .first()
    )
    if obj:
        return obj
    city = City()
    city.department_code = city_data["department_code"]
    city.name = city_data["name"]
    db.session.add(city)
    db.session.commit()
    return city


def update(obj, data):
    for key, value in data.dict().items():
        if value == 'null':
            setattr(obj, key, None)
        elif value is not None:
            setattr(obj, key, value)
    return obj


def create_hospitals(hospital, city, data):
    hospital.city_id = city.id
    hospital.name = data["name"]
    hospital.phone_number = data["phone_number"]
    return hospital


@bp.get('/')
def get_hospitals(name: str = None, city_id: int = None):
    query = db.session.query(Hospital)
    if name:
        query = query.filter(Hospital.name.ilike(f'%{name}%'))
    if city_id:
        query = query.filter_by(city_id=city_id)
    return query


@bp.get('/<int:hospital_id>')
def get_hospital(hospital_id):
    result = db.session.get(Hospital, hospital_id)
    if not result:
        raise NotFoundError.r("La ressource n'a pas été trouvée")
    return result


@bp.post('/')
def create_hospital(data):
    city_data = data.pop('city')
    city = create_city(city_data)
    hospital = Hospital()
    hospital = create_hospitals(hospital, city, data)
    hospital.refresh_coordinates()
    db.session.add(hospital)
    db.session.commit()
    return get_hospital(hospital.id)


@bp.delete('/<int:id>')
def delete_listing(id: int):
    hospital = get_hospital(id)
    db.session.delete(hospital)
    db.session.commit()


@bp.post('/<int:id>')
def update_hospital(id: int, data: dict):
    hospital = get_hospital(id)
    for key, value in data.items():
        if value == 'null':
            setattr(hospital, key, None)
        elif value is not None:
            if key == 'city':
                city = create_city(value)
                setattr(hospital, 'city_id', city.id)
            else:
                setattr(hospital, key, value)
    hospital.refresh_coordinates()
    db.session.commit()
