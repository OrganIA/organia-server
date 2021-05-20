from fastapi import APIRouter

from app import db
from app.errors import NotFoundError
from app.models import (
    Person, PersonSchema, PersonCreateSchema, PersonUpdateSchema
)

router = APIRouter(prefix='/persons')


@router.get('/')
async def get_persons():
    return db.session.query(Person).all()


@router.get('/{person_id}')
async def get_person(person_id: int):
    return db.session.get(Person, person_id) or NotFoundError.r()


@router.post('/', status_code=201)
async def create_person(person: PersonCreateSchema):
    person = Person(**person.dict())
    db.session.add(person)
    db.session.commit()
    return await get_person(person.id)


@router.post('/{person_id}', response_model=PersonSchema)
async def update_person(person_id: int, data: PersonUpdateSchema):
    person = await get_person(person_id)
    person.update(data)
    db.session.commit()
    return person


@router.delete('/{person_id}')
async def delete_person(person_id: int):
    person = await get_person(person_id)
    db.session.delete(person)
    db.session.commit()
