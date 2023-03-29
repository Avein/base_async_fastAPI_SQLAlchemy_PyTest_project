from typing import AsyncGenerator, Optional
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.orm import sessionmaker


class SessionInitializationError(Exception):
    ...


class _Session:
    def __init__(self) -> None:
        self._session: Optional[sessionmaker] = None

    def set_engine(self, engine: AsyncEngine) -> None:
        self._session = sessionmaker(
            engine,
            expire_on_commit=False,
            class_=AsyncSession,
            autocommit=False,
            autoflush=True,
            future=True,
        )

    @property
    def session(self) -> sessionmaker:
        if not self._session:
            raise SessionInitializationError(
                "Session is not initialized. Probably engine is not set up"
            )
        return self._session

    async def __call__(self) -> AsyncSession:
        async with self.session() as session:
            yield session

    @asynccontextmanager
    async def transaction(self, autocommit: bool = True) -> AsyncGenerator:
        async with self.session() as session:
            await session.begin()
            yield session
            if autocommit:
                await session.commit()


Session = _Session()
TestSession = _Session()
