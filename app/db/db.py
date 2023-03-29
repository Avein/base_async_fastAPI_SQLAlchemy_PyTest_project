from typing import TypeVar, Type

import inflect
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, DateTime, Integer, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.declarative import declared_attr

from app.db.session import Session, TestSession
from app.envs import Env


engine = create_async_engine(
    Env.db.POSTGRES_URL, isolation_level="REPEATABLE READ",
    pool_size=5,
    max_overflow=10,
    pool_recycle=-1,
    pool_timeout=30
)
Session.set_engine(engine)

test_engine = create_async_engine(
    Env.db.POSTGRES_TEST_URL, isolation_level="REPEATABLE READ",
    pool_size=5,
    max_overflow=10,
    pool_recycle=-1,
    pool_timeout=30
)
TestSession.set_engine(engine=test_engine)


inflect_engine = inflect.engine()
SchemaType = TypeVar("SchemaType", bound=BaseModel)
ModelType = TypeVar("ModelType", bound='Base')


class ORMBase(object):
    __name__: str

    @declared_attr
    def __tablename__(cls):
        return inflect_engine.plural(cls.__name__.lower())

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    created_on = Column(DateTime, default=func.now())
    updated_on = Column(DateTime, default=func.now(), onupdate=func.now())

    @classmethod
    def from_schema(cls: Type[ModelType], obj: Type[SchemaType]) -> ModelType:
        return cls(**jsonable_encoder(obj))

    async def save(self: Type[ModelType], db: AsyncSession, commit: bool = False) -> ModelType:
        db.add(self)
        await db.flush()
        await db.refresh(self)
        if commit:
            await db.commit()
        return self

    async def remove(self: Type[ModelType], db: AsyncSession, commit: bool = False) -> ModelType:
        await db.delete(self)
        if commit:
            await db.commit()
        return self


Base = declarative_base(cls=ORMBase)
