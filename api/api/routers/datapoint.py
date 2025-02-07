from typing import Annotated

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from api.db import get_session
from model.model import DatapointPublic, DatapointCreate, Datapoint, DatapointUpdate

router = APIRouter(
    prefix="/api/datapoints",
    tags=["datapoints"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[DatapointPublic])
async def get_datapoints(
    session: AsyncSession = Depends(get_session),
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    result = await session.exec(select(Datapoint).offset(offset).limit(limit))
    data = result.all()
    return data


@router.post("/", response_model=DatapointPublic)
async def create_datapoint(
    datapoint: DatapointCreate,
    session: AsyncSession = Depends(get_session),
):
    db_object = Datapoint.model_validate(datapoint)
    session.add(db_object)
    await session.commit()
    await session.refresh(db_object)
    return db_object


@router.patch("/{id}", response_model=DatapointPublic)
async def update_datapoint(
    id: int,
    datapoint: DatapointUpdate,
    session: AsyncSession = Depends(get_session),
):
    datapoint_db = await session.get(Datapoint, id)
    if not datapoint_db:
        raise HTTPException(status_code=404, detail="Datapoint not found")
    datapoint_data = datapoint.model_dump(exclude_unset=True)
    datapoint_db.sqlmodel_update(obj=datapoint_data)
    session.add(datapoint_db)
    await session.commit()
    await session.refresh(datapoint_db)
    return datapoint_db


@router.delete("/{id}")
async def delete_datapoint(
    id: int,
    session: AsyncSession = Depends(get_session),
):
    datapoint = await session.get(Datapoint, id)
    if not datapoint:
        raise HTTPException(status_code=404, detail="Datapoint not found")
    await session.delete(datapoint)
    await session.commit()
    return {"ok": True}
