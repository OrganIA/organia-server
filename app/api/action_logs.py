from fastapi import APIRouter, Depends

from app.models import ActionLog
from .dependencies import get_db


router = APIRouter(prefix='/logs')


@router.get('/')
async def get_logs(session=Depends(get_db)):
    return (
        session.query(ActionLog)
        .order_by(ActionLog.created_at.desc())
    ).all()
