from app import db
from app.db.models import Person
from app.errors import NotFoundError
from app.utils.bp import Blueprint
from app.utils.static import Static

bp = Blueprint('persons', auth=False)


class PersonSchema(Static):
    first_name = str
    last_name = str
    birth_date = str
    description = str
    abo = str
    rhesus = str
    gender = str


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


@bp.post('/{person_id}')
async def update_person(person_id, data):
    person = await get_person(person_id)
    person.update(data)
    db.session.commit()
    return person


@bp.delete('/{person_id}')
async def delete_person(person_id: int):
    person = await get_person(person_id)
    db.session.delete(person)
    db.session.commit()
