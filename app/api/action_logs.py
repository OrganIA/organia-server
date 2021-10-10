from fastapi import APIRouter

from app import db
from app.models import ActionLog


router = APIRouter(prefix='/logs')


@router.get('/')
async def get_logs():
    return (
        db.session.query(ActionLog)
        .order_by(ActionLog.created_at.desc())
    ).all()
