from typing import List
from fastapi import APIRouter

from app import db
from typing import Optional
from app.errors import NotFoundError
from app.models import Hospital
from app.api.schemas.hospital import (
    HospitalSchema,
)

router = APIRouter(prefix='/hospitals')

@router.get('/')
async def get_hospitals(name: Optional[str] = None, city: Optional[str] = None):
    query = db.session.query(Hospital)
    if name:
        query = query.filter(Hospital.name.ilike(f'%{name}%'))
    if city:
        query = query.filter(Hospital.city.ilike(f'%{city}%'))
    return query.all() or NotFoundError.r('Hospital not found.')

@router.get('/{id}')
async def get_hospital(id: int):
    return db.session.get(Hospital, id) or NotFoundError.r()

@router.post('/', status_code=201)
async def create_hospital(hospital: HospitalSchema):
    hospital = Hospital(**hospital.dict())
    db.session.add(hospital)
    db.session.commit()
    return await get_hospital(hospital.id)