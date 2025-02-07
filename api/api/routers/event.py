from typing import Annotated

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from api.db import get_session
from model.model import EventPublic, EventCreate, Event, EventUpdate

router = APIRouter(
    prefix="/api/events",
    tags=["events"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[EventPublic])
async def get_events(
    session: AsyncSession = Depends(get_session),
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    result = await session.exec(select(Event).offset(offset).limit(limit))
    data = result.all()
    return data


@router.post("/", response_model=EventPublic)
async def create_event(
    event: EventCreate,
    session: AsyncSession = Depends(get_session),
):
    db_object = Event.model_validate(event)
    session.add(db_object)
    await session.commit()
    await session.refresh(db_object)
    return db_object


@router.get("/{id}", response_model=EventPublic)
async def get_event(
    id: int,
    session: AsyncSession = Depends(get_session),
):
    event_db = await session.get(Event, id)
    if not event_db:
        raise HTTPException(status_code=404, detail="Event not found")
    return event_db


@router.put("/{id}", response_model=EventPublic)
@router.patch("/{id}", response_model=EventPublic)
async def update_event(
    id: int,
    event: EventUpdate,
    session: AsyncSession = Depends(get_session),
):
    event_db = await session.get(Event, id)
    if not event_db:
        raise HTTPException(status_code=404, detail="Event not found")
    event_data = event.model_dump(exclude_unset=True)
    event_db.sqlmodel_update(obj=event_data)
    session.add(event_db)
    await session.commit()
    await session.refresh(event_db)
    return event_db


@router.delete("/{id}")
async def delete_event(
    id: int,
    session: AsyncSession = Depends(get_session),
):
    event = await session.get(Event, id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    await session.delete(event)
    await session.commit()
    return {"ok": True}
