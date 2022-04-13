from typing import List
from fastapi import APIRouter

from app import db
from typing import Optional
from app.distance import get_distance
from app.errors import NotFoundError
from app.models import City, Hospital, Listing
from app.api.schemas.hospital import (
    HospitalSchema,
    HospitalGetSchema,
    HospitalUpdateSchema,
)
from .dependencies import logged_user


router = APIRouter(prefix='/hospitals', dependencies=[logged_user])


@router.get('/', response_model=List[HospitalGetSchema])
async def get_hospitals(
    name: Optional[str] = None, city_id: Optional[int] = None
):
    query = db.session.query(Hospital)
    if name:
        query = query.filter(Hospital.name.ilike(f'%{name}%'))
    if city_id:
        query = query.filter_by(city_id=city_id)
    return query.all()


@router.get('/{hospital_id}', response_model=HospitalGetSchema)
async def get_hospital(hospital_id: int):
    return db.get(Hospital, hospital_id, error_on_unfound=True)


@router.post('/', status_code=201, response_model=HospitalSchema)
async def create_hospital(hospital: HospitalSchema):
    data = hospital.dict()
    city_data = data.pop('city')
    city = db.get_or_create(
        City,
        {'department_code': city_data['department_code']},
        {'name': city_data['name']},
    )
    data['city'] = city
    hospital = db.add(Hospital, data)
    return await get_hospital(hospital.id)


@router.post('/{hospital_id}', response_model=HospitalGetSchema)
async def update_hospital(
    hospital_id: int, data: HospitalUpdateSchema,
):
    data = data.dict()
    data_test = data.pop('city')
    hospital = await get_hospital(hospital_id)
    hospital.update(data)
    db.session.commit()
    return hospital

@router.delete('/{hospital_id}')
async def delete_hospital(hospital_id: int):
    hospital = await get_hospital(hospital_id)
    db.delete(hospital)
    db.session.commit()


@router.get('/hospital/distance')
async def get_distance_hospital(first_city: str, second_city: str):
    return get_distance(first_city, second_city) or NotFoundError.r()
