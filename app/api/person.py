from datetime import datetime

from app import db
from app.db.models import Person
from app.errors import NotFoundError
from app.utils.bp import Blueprint
from app.utils.static import Static

bp = Blueprint(__name__)


class PersonSchema(Static):
    @staticmethod
    def birth_date(d):
        birth_date = Static._get(d, 'birth_date')
        return datetime.fromisoformat(birth_date).date()

    first_name = str
    last_name = str
    description = str
    abo = Person.ABO
    rhesus = Person.Rhesus
    gender = Person.Gender


def update(person, data):
    for key, value in data.dict.items():
        if value == 'null':
            setattr(person, key, None)
        elif value is not None:
            setattr(person, key, value)
    return person


@bp.get('/')
def get_persons():
    return db.session.query(Person)


@bp.get('/<int:id>')
def get_person(id):
    result = db.session.get(Person, id)
    if not result:
        raise NotFoundError
    return result


@bp.post('/')
def create_person(data: PersonSchema):
    person = Person(**data.dict)
    db.session.add(person)
    db.session.commit()
    return get_person(person.id)


@bp.post('/<int:id>')
def update_person(id, data: PersonSchema):
    person = db.session.get(Person, id)
    person_update = update(person, data)
    db.session.commit()
    return person_update


@bp.delete('/<int:id>')
def delete_person(id: int):
    person = get_person(id)
    db.session.delete(person)
    db.session.commit()
