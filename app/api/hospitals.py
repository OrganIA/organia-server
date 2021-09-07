from typing import List
from fastapi import APIRouter

from app import db
from app.errors import NotFoundError
from app.models import Hospital
from app.api.schemas.hospital import (
    HospitalSchema,
)

router = APIRouter(prefix='/hospitals')

@router.get('/')
async def get_hospitals():
    return db.session.query(Hospital).all()

@router.get('/{hospital_name}')
async def get_hospital(hospital_name: str):
    return db.session.query(Hospital).filter_by(name=hospital_name).all() or NotFoundError.r()

@router.post('/', status_code=201)
async def create_hospital(hospital: HospitalSchema):
    hospital = Hospital(**hospital.dict())
    db.session.add(hospital)
    db.session.commit()
    return await get_hospital(hospital.name)