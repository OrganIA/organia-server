from fastapi import APIRouter

from app.errors import NotFoundError
from app.models import Lung

router = APIRouter(prefix='/organs')


@router.get('/{organ_name}')
async def get_organ_required_fields(organ_name: str):

    print(organ_name)
    if organ_name == 'lungs':
        return Lung.__table__.columns.keys()
    else:
        raise NotFoundError('No such organ found')
