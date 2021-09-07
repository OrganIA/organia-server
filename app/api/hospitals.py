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
    if name == None and city == None:
        return db.session.query(Hospital).all()
    filters = db.session.query(Hospital).filter(
        Hospital.name.ilike(f'%{name}%')
        | Hospital.city.ilike(f'%{city}%')
    ).all() or NotFoundError.r('Hospital not found.')
    return filters

@router.get('/{hospital_id}')
async def get_hospital(hospital_id: int):
    return db.session.query(Hospital).filter_by(id=hospital_id).all() or NotFoundError.r()

@router.post('/', status_code=201)
async def create_hospital(hospital: HospitalSchema):
    hospital = Hospital(**hospital.dict())
    db.session.add(hospital)
    db.session.commit()
    return await get_hospital(hospital.id)