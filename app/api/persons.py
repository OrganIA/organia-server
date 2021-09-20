from typing import List
from fastapi import APIRouter

from app import db
from app.errors import NotFoundError
from app.models import Person
from app.api.schemas.person import (
    PersonSchema, PersonGetSchema, PersonUpdateSchema, PersonUpdateScoring,
)
from .dependencies import logged_user

router = APIRouter(prefix='/persons', dependencies=[logged_user])


@router.get('/', response_model=List[PersonGetSchema])
async def get_persons():
    return db.session.query(Person).all()


@router.get('/{person_id}', response_model=PersonGetSchema)
async def get_person(person_id: int):
    return db.session.get(Person, person_id) or NotFoundError.r()


@router.post('/', status_code=201)
async def create_person(person: PersonSchema):
    person = Person(**person.dict())
    db.session.add(person)
    db.session.commit()
    return await get_person(person.id)


@router.post('/{person_id}', response_model=PersonGetSchema)
async def update_person(person_id: int, data: PersonUpdateSchema):
    person = await get_person(person_id)
    person.update(data)
    db.session.commit()
    return person


@router.post('/{person_id}', response_model=PersonGetSchema)
async def update_scoring(person_id: int, data: PersonUpdateScoring):
    person = await get_person(person_id)
    person.update(data)
    db.session.commit()
    return person


@router.delete('/{person_id}')
async def delete_person(person_id: int):
    person = await get_person(person_id)
    db.session.delete(person)
    db.session.commit()
