from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from api.db import get_session
from model.model import DatapointPublic, DatapointCreate, Datapoint

router = APIRouter(
    prefix="/datapoints",
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
    db_object= Datapoint.model_validate(datapoint)
    session.add(db_object)
    await session.commit()
    await session.refresh(db_object)
    return db_object