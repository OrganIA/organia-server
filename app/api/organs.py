from fastapi import APIRouter

from app.errors import NotFoundError
from app.models import Lung, HeartScore, Kidney

router = APIRouter(prefix='/organs')


@router.get('/{organ_name}')
async def get_organ_required_fields(organ_name: str):
    match organ_name:
        case 'lung':
            return Lung.__table__.columns.keys()
        case 'heart':
            return HeartScore.__table__.columns.keys()
        case 'kidney':
            return Kidney.__table__.columns.keys()
        case _:
            raise NotFoundError