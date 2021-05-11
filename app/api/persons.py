from fastapi import APIRouter

from app import db
from app.models import Person

router = APIRouter(prefix='/persons')


@router.get('/')
async def get_persons():
    return db.session.query(Person).all()


@router.get('/{person_id}')
async def get_person(person_id: int):
    return db.get_or_404(Person, person_id)


@router.delete('/{person_id}')
async def delete_person(person_id: int):
    person = await get_person(person_id)
    db.session.delete(person)
    db.session.commit()
