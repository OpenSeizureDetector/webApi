import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlmodel import select, desc
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
    start_date: Annotated[
        datetime.datetime | None,
        Query(description="Start date to filter events. Cannot be in the future."),
    ] = None,
    end_date: Annotated[
        datetime.datetime | None,
        Query(
            description="End date to filter events. Must be later than start_date if both are provided."
        ),
    ] = None,
    duration: Annotated[
        int | None,
        Query(
            ge=0,
            description="Duration in minutes to filter events. Must be a positive integer.",
        ),
    ] = None,
    event_to_categorize: bool = Query(
        True, description="Restrict to events that need categorization (type is None)."
    ),
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    """
    Retrieve a list of events with optional filtering by date range, duration, and categorization status.
    The results are paginated with `offset` and `limit`.
    """

    # Ensure start_date is not in the future
    now = datetime.datetime.now(datetime.UTC)
    if start_date is not None and start_date > now:
        raise HTTPException(
            status_code=422, detail="Start date cannot be in the future."
        )

    # Ensure end_date is not earlier than start_date
    if start_date is not None and end_date is not None and end_date < start_date:
        raise HTTPException(
            status_code=422, detail="End date cannot be earlier than start date."
        )

    # Convert duration to timedelta if provided
    if duration is not None:
        duration_delta = datetime.timedelta(minutes=duration)

        # Apply duration logic based on available dates
        if start_date is None and end_date is None:
            end_date = now
            start_date = end_date - duration_delta
        elif start_date is not None and end_date is None:
            end_date = start_date + duration_delta
        elif end_date is not None and start_date is None:
            start_date = end_date - duration_delta

    # Create the base query
    statement = select(Event).offset(offset).limit(limit)

    result1 = await session.exec(statement)
    data1 = result1.all()
    # Apply start_date filter if provided
    if start_date is not None:
        statement = statement.where(Event.dataTime >= start_date)

    # Apply end_date filter if provided
    if end_date is not None:
        statement = statement.where(Event.dataTime <= end_date)

    # Filter events that need categorization (i.e., type is None)
    if event_to_categorize:
        statement = statement.where(Event.type.is_(None))

    # Order results by descending event date
    statement = statement.order_by(desc(Event.dataTime))

    # Execute the query
    result = await session.exec(statement)
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
