from app.db import session
from app.db.models import ActionLog
from app.utils.bp import Blueprint

bp = Blueprint(__name__, prefix="/logs")


@bp.get("/")
def get_logs():
    return (
        session.query(ActionLog).order_by(ActionLog.created_at.desc())
    ).all()
