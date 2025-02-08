from datetime import datetime
from typing import Any

from sqlalchemy import Column, DateTime, func, JSON
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


######################### EVENT ####################################
class EventBase(SQLModel):
    osdAlarmState: int | None = Field(None)
    userId: int | None = Field(default=None, foreign_key="user.id")
    dataTime: datetime | None = Field(None)
    type: str | None = Field(None)
    subType: str | None = Field(None)
    desc: str | None = Field(None)
    dataJSON: dict[str, Any] | None = Field(
        sa_column=Column(JSON), default_factory=dict
    )


class Event(EventBase, table=True):
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
    user: User | None = Relationship(back_populates="events")
    datapoints: list["Datapoint"] = Relationship(back_populates="event")


class EventPublic(EventBase):
    id: int
    created: datetime
    updated: datetime


class EventCreate(EventBase): ...


class EventUpdate(EventBase): ...


######################### DATAPOINT ####################################
class DatapointBase(SQLModel):
    dataTime: datetime | None = Field(None, index=True)
    # userId: int | None = Field(default=None, foreign_key="user.id")
    statusStr: str = Field(default="", index=True, max_length=30)
    accMean: float | None = Field(None)
    accSd: float | None = Field(None)
    hr: float | None = Field(None)
    categoryId: int | None = Field(None)
    # eventId: int | None = Field(None)
    dataJSON: dict[str, Any] | None = Field(
        sa_column=Column(JSON), default_factory=dict
    )


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
    event: Event | None = Relationship(back_populates="datapoints")
    event_id: int | None = Field(default=None, foreign_key="event.id")


class DatapointPublic(DatapointBase):
    id: int
    created: datetime
    updated: datetime


class DatapointCreate(DatapointBase): ...


class DatapointUpdate(DatapointBase):
    statusStr: str | None = Field(None)
