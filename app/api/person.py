from datetime import date

from pydantic import BaseModel

from app import db
from app.db.models import Person
from app.errors import NotFoundError
from app.utils.bp import Blueprint

bp = Blueprint(__name__)


class PersonSchema(BaseModel):
    first_name: str | None
    last_name: str | None
    birth_date: date | None
    description: str | None
    abo: Person.ABO | None
    rhesus: Person.Rhesus | None
    gender: Person.Gender | None


class PersonCreateSchema(PersonSchema):
    first_name: str
    last_name: str
    birth_date: date
    abo: Person.ABO
    rhesus: Person.Rhesus


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
def create_person(data: PersonCreateSchema):
    person = Person(**data.dict())
    db.session.add(person)
    db.session.commit()
    return get_person(person.id)


@bp.post('/<int:id>')
def update_person(id, data: PersonSchema):
    person = get_person(id)
    person.read_dict(data.dict(exclude_unset=True))
    db.session.commit()
    return person


@bp.delete('/<int:id>')
def delete_person(id: int):
    person = get_person(id)
    db.session.delete(person)
    db.session.commit()
