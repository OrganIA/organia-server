from typing import List
from fastapi import APIRouter

from app import db
from typing import Optional
from app.errors import NotFoundError
from app.models import Hospital, City
from app.api.schemas.hospital import (
    HospitalSchema,
)

router = APIRouter(prefix='/hospitals')


@router.get('/')
async def get_hospitals(name: Optional[str] = None, city_id: Optional[int] = None):
    query = db.session.query(Hospital)
    if name:
        query = query.filter(Hospital.name.ilike(f'%{name}%'))
    if city_id:
        query = query.filter_by(city_id=city_id)
    return query.all() or NotFoundError.r('Hospital not found.')


@router.get('/{hospital_id}')
async def get_hospital(hospital_id: int):
    return db.session.get(Hospital, hospital_id) or NotFoundError.r()


@router.post('/', status_code=201)
async def create_hospital(hospital: HospitalSchema):
    hospital = Hospital(**hospital.dict())
    db.session.add(hospital)
    db.session.commit()
    return await get_hospital(hospital.id)


@router.delete('/{hospital_id}')
async def delete_hospital(hospital_id: int):
    hospital = await get_hospital(hospital_id)
    db.session.delete(hospital)
    db.session.commit()
