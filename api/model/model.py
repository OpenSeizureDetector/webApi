from datetime import datetime

from sqlalchemy import Column, DateTime, func
from sqlmodel import SQLModel, Field, Relationship


######################### USER ####################################
class UserBase(SQLModel):
    created: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )
    updated: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            server_onupdate=func.now(),
        )
    )
    name: str | None
    # dataJSON = models.TextField(blank=True, null=True)


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    datapoints: list["Datapoint"] = Relationship(back_populates="user")
    events: list["Event"] = Relationship(back_populates="user")


class UserPublic(UserBase):
    id: int


class UserCreate(UserBase): ...


class UserUpdate(UserBase): ...


######################### DATAPOINT ####################################
class DatapointBase(SQLModel):
    dataTime: datetime | None = Field(None)
    # userId: int | None = Field(default=None, foreign_key="user.id")
    statusStr: str = Field(default="", index=True, max_length=30)
    accMean: float | None = Field(None)
    accSd: float | None = Field(None)
    hr: float | None = Field(None)
    categoryId: int | None = Field(None)
    eventId: int | None = Field(None)
    # dataJSON = models.TextField(blank=True, null=True) = Field(None)


class Datapoint(DatapointBase, table=True):
    created: datetime | None = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), server_default=func.now()),
    )
    updated: datetime | None = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            server_onupdate=func.now(),
        ),
    )
    id: int | None = Field(default=None, primary_key=True)
    user: User | None = Relationship(back_populates="datapoints")
    user_id: int | None = Field(default=None, foreign_key="user.id")


class DatapointPublic(DatapointBase):
    id: int
    created: datetime
    updated: datetime


class DatapointCreate(DatapointBase): ...


class DatapointUpdate(DatapointBase):
    statusStr: str | None = Field(None)


######################### EVENT ####################################
class EventBase(SQLModel):
    created: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )
    updated: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            server_onupdate=func.now(),
        )
    )

    osdAlarmState: int | None
    userId: int | None = Field(default=None, foreign_key="user.id")
    dataTime: datetime | None
    type: str | None
    subType: str | None
    desc: str | None
    # dataJSON = models.TextField(blank=True, null=True)


class Event(EventBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user: User | None = Relationship(back_populates="events")


class EventPublic(EventBase):
    id: int


class EventCreate(EventBase): ...


class EventUpdate(EventBase): ...
