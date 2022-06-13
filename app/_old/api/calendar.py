from typing import List
from fastapi import APIRouter, Depends

from app import db
from app.api.schemas.calendar import (
    CalendarEventSchema, CalendarEventCreateSchema
)
from app.errors import Unauthorized
from app.models import CalendarEvent, User
from .dependencies import get_db, get_user

router = APIRouter(prefix='/calendar')


@router.get('/', response_model=List[CalendarEventSchema])
async def get_events(user=Depends(get_user), session=Depends(get_db)):
    return session.query(CalendarEvent).filter_by(author=user).all()


@router.get('/{event_id}', response_model=CalendarEventSchema)
async def get_event(event_id: int, user=Depends(get_user), session=Depends(get_db)):
    event = db.get(
        CalendarEvent, event_id, error_on_unfound=True, session=session
    )
    if event.author != user:
        raise Unauthorized
    return event


@router.post('/', status_code=201, response_model=CalendarEventSchema)
async def create_event(event: CalendarEventCreateSchema, user=Depends(get_user), session=Depends(get_db)):
    db_event = db.add(CalendarEvent, event.dict() | {'author': user}, session=session)
    return await get_event(db_event.id)


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
