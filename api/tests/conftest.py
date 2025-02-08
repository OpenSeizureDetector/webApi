import asyncio
from asyncio import current_task
from collections.abc import AsyncGenerator
from typing import Iterator

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncConnection,
    async_scoped_session,
)
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from api.api import app
from api.db import get_session


@pytest_asyncio.fixture(scope="session")
async def async_db_connection() -> AsyncGenerator[AsyncConnection, None]:
    database_dsn = "sqlite+aiosqlite:///testing.db"
    async_engine = create_async_engine(
        database_dsn, connect_args={"check_same_thread": False}, echo=False, future=True
    )

    async with async_engine.begin() as conn:
        # separate connection because .create_all makes .commit inside
        await conn.run_sync(SQLModel.metadata.create_all)

    conn = await async_engine.connect()
    try:
        yield conn
    except:
        raise
    finally:
        await conn.rollback()

    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)

    await async_engine.dispose()


async def __session_within_transaction(
    async_db_connection: AsyncConnection,
) -> AsyncGenerator[AsyncSession, None]:
    async_session_maker = async_sessionmaker(
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
        bind=async_db_connection,
        class_=AsyncSession,
    )
    transaction = await async_db_connection.begin()
    async with async_session_maker() as session:
        yield session

    # no need to truncate, all data will be rolled back
    await transaction.rollback()


@pytest_asyncio.fixture(scope="function")
async def async_db_session(
    async_db_connection: AsyncConnection,
) -> AsyncGenerator[AsyncSession, None]:
    async for session in __session_within_transaction(async_db_connection):
        # setup some data per function
        yield session


@pytest_asyncio.fixture(scope="function")
async def async_client(async_db_session: AsyncSession) -> AsyncClient:
    """Setup the test client for the FastAPI app.

    Returns:
        AsyncClient: the async httpx test client to use in the tests.
    """

    def override_get_db() -> Iterator[async_scoped_session]:
        """Utility function to wrap the database session in a generator.

        Yields:
            Iterator[AsyncSession]: An iterator containing one database session.
        """
        yield async_db_session

    app.dependency_overrides[get_session] = override_get_db
    return AsyncClient(transport=ASGITransport(app=app), base_url="http://localhost")


@pytest.fixture(scope="session")
def event_loop():
    """Créer un nouvel event loop pour les tests"""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()
