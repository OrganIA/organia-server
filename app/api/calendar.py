from datetime import datetime

from app import auth, db
from app.db.models import CalendarEvent, User
from app.errors import NotFoundError, Unauthorized
from app.utils.bp import Blueprint
from app.utils.static import Static

bp = Blueprint(__name__)


class CalendarEventSchema(Static):
    @staticmethod
    def start_date(d):
        start_date = Static._get(d, 'start_date')
        return datetime.fromisoformat(start_date)

    def end_date(d):
        end_date = Static._get(d, 'end_date')
        return datetime.fromisoformat(end_date)

    title = str
    description = str
    event_type = str


@bp.get('/')
@auth.route()
def get_events(auth_user: User):
    return db.session.query(CalendarEvent).filter_by(author=auth_user)


@bp.get('/<int:event_id>')
@auth.route()
def get_event(event_id: int, auth_user):
    event = db.session.get(CalendarEvent, event_id)
    if not event:
        raise NotFoundError
    if event.author_id != auth_user.id:
        raise Unauthorized
    return event


@bp.post('/')
@auth.route()
def create_event(data: CalendarEventSchema, auth_user: User):
    event = CalendarEvent(**data.dict, author=auth_user)
    db.session.add(event)
    db.session.commit()
    return event


@bp.post('/<int:event_id>')
@auth.route()
def update_event(
    event_id: int,
    data: dict,
    auth_user: id,
):
    event = db.session.get(CalendarEvent, event_id)
    if event.author_id != auth_user.id:
        raise Unauthorized
    for key, value in data.items():
        if key == 'start_date' or key == 'end_date':
            value = datetime.fromisoformat(value)
        setattr(event, key, value)
    db.session.commit()
    return event


@bp.delete('/<int:event_id>')
@auth.route()
def delete_event(event_id: int, auth_user: User):
    event = db.session.get(CalendarEvent, event_id)
    if event.author_id != auth_user.id:
        raise Unauthorized
    db.session.delete(event)
    db.session.commit()
