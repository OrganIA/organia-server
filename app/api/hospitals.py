from app import db, geopy
from app.db.actions.get_or_create import get_or_create as _get_or_create
from app.db.models import City, Hospital
from app.errors import NotFoundError
from app.utils.bp import Blueprint
from app.utils.static import Static

bp = Blueprint("hospitals", auth=False)


class HospitalSchema(Static):
    name = str
    phone_number = str
    latitude = float
    longitude = float
    city_id = int


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
    for key, value in data.dict.items():
        if value == 'null':
            setattr(obj, key, None)
        elif value is not None:
            setattr(obj, key, value)
    return obj


def create_hospitals(hospital, data):
    hospital.city_id = data["city_id"]
    hospital.name = data["name"]
    hospital.phone_number = data["phone_number"]
    hospital.latitude = data["latitude"]
    hospital.longitude = data["longitude"]
    position = geopy.get_coordinates(hospital.name)
    if position:
        hospital.latitude = position[0]
        hospital.longitude = position[1]
    else:
        raise NotFoundError.r("L'addresse est incorrecte")
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
    create_city(city_data)
    hospital = Hospital()
    hospital = create_hospitals(hospital, data)
    db.session.add(hospital)
    db.session.commit()
    return get_hospital(hospital.id)


@bp.delete('/<int:id>')
def delete_listing(id: int):
    hospital = get_hospital(id)
    db.session.delete(hospital)
    db.session.commit()
