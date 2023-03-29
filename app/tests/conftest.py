import asyncio
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.artists import crud
from app.db.db import test_engine, Base
from app.db.session import Session, TestSession
from app.main import app
from app.tests.fixtures import artists_fixtures

app.dependency_overrides[Session] = TestSession


@pytest_asyncio.fixture
async def async_client():
    async with AsyncClient(app=app, follow_redirects=True) as client:
        yield client


@pytest_asyncio.fixture
async def session() -> AsyncGenerator:
    async with TestSession.session() as session:
        yield session


@pytest_asyncio.fixture(autouse=True)
async def seed_db(session: AsyncSession) -> None:
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    for artist in artists_fixtures:
        await crud.create_artist(session, artist)


@pytest.fixture(scope="module")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()
