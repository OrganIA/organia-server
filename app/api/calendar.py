from typing import List
from fastapi import APIRouter

from app import db
from app.api.schemas.calendar import (
    CalendarEventSchema, CalendarEventCreateSchema
)
from app.errors import Unauthorized
from app.models import CalendarEvent, User
from .dependencies import logged_user

router = APIRouter(prefix='/calendar')


@router.get('/', response_model=List[CalendarEventSchema])
async def get_events(logged_user: User = logged_user):
    return db.session.query(CalendarEvent).filter_by(author=logged_user).all()


@router.get('/{event_id}', response_model=CalendarEventSchema)
async def get_event(event_id: int, logged_user: User = logged_user):
    event = db.get(CalendarEvent, event_id, error_on_unfound=True)
    if event.author != logged_user:
        raise Unauthorized
    return event


@router.post('/', status_code=201, response_model=CalendarEventSchema)
async def create_event(
        event: CalendarEventCreateSchema, logged_user: User = logged_user
):
    db_event = db.add(CalendarEvent, event.dict() | {'author': logged_user})
    return await get_event(db_event.id, logged_user=logged_user)


@router.post('/{event_id}', status_code=201, response_model=CalendarEventSchema)
async def update_event(
    event_id: int,
    data: CalendarEventCreateSchema,
    logged_user: User = logged_user
):
    event = await get_event(event_id, logged_user=logged_user)
    if event.author != logged_user:
        raise Unauthorized
    event.update(data)
    db.session.commit()
    return event


@router.delete('/{event_id}')
async def delete_event(event_id: int, logged_user: User = logged_user):
    event = await get_event(event_id, logged_user=logged_user)
    if event.author != logged_user:
        raise Unauthorized
    db.delete(event)
