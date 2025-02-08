from datetime import datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlmodel import select, desc
from sqlmodel.ext.asyncio.session import AsyncSession

from api.db import get_session
from model.model import DatapointPublic, Datapoint

router = APIRouter(
    prefix="/api/dataSummary",
    tags=["dataSummary"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.get(
    "/",
    response_model=list[DatapointPublic],
    summary="Retrieve datapoints summary",
    description="Fetch a list of datapoints with optional filtering by date and duration.",
)
async def get_datapoints_summary(
    session: AsyncSession = Depends(get_session),
    user: int = Query(
        None,
        deprecated=True,
        description="Previously used to filter by user ID. Should be ignored.",
    ),
    startDateStr: str = Query(
        None,
        deprecated=True,
        description="Start date as a string (format YYYY-MM-DD HH:MM:SS). Use 'start_date' instead.",
    ),
    endDateStr: str = Query(
        None,
        deprecated=True,
        description="End date as a string (format YYYY-MM-DD HH:MM:SS). Use 'end_date' instead.",
    ),
    durationMinStr: str = Query(
        None,
        deprecated=True,
        description="Duration in minutes as a string. Use 'duration_min' instead.",
    ),
    start_date: datetime = Query(
        None,
        description="Start date to filter datapoints (overrides 'startDateStr' if both are provided).",
    ),
    end_date: datetime = Query(
        None,
        description="End date to filter datapoints (overrides 'endDateStr' if both are provided).",
    ),
    duration: timedelta = Query(None, description="Duration to filter datapoints."),
    offset: int = Query(0, description="Number of records to skip (default: 0)."),
    limit: int = Query(
        100,
        le=100,
        description="Maximum number of records to return (default: 100, max: 100).",
    ),
):
    """Retrieve a summary of datapoints with optional filtering."""
    statement = select(Datapoint).offset(offset).limit(limit)

    # we should ignore the user parameter. A user should never access other user data.
    # user_id = get_current_user_id
    # startDateStr and endDateStr are deprecated, but until the application are all migrated,
    # we need to keep them available
    if start_date is None and startDateStr is not None:
        start_date = datetime.strptime(startDateStr, "%Y-%m-%d %H:%M:%S")

    if end_date is None and endDateStr is not None:
        end_date = datetime.strptime(endDateStr, "%Y-%m-%d %H:%M:%S")

    if duration is None and durationMinStr is not None:
        try:
            duration = timedelta(minutes=int(durationMinStr))
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid durationMinStr format")

    if duration is not None:
        if start_date is not None and end_date is None:
            end_date = start_date + duration
        if end_date is not None and start_date is None:
            start_date = end_date - duration

    result1 = await session.exec(statement=statement)
    data1 = result1.all()
    # Applying date filtering
    if start_date is not None:
        statement = statement.where(Datapoint.dataTime >= start_date)

    if end_date is not None:
        statement = statement.where(Datapoint.dataTime <= end_date)

    # order by decreasing date
    statement = statement.order_by(desc(Datapoint.dataTime))
    result = await session.exec(statement=statement)
    data = result.all()
    return data
