import asyncio
from datetime import datetime, timedelta

from fastapi import FastAPI

from app.api import init_routers
from app.api.artists.tasks import fetch_top_artists
from app.db.db import engine, Base
from app.db.session import Session

app = FastAPI()

init_routers(app)


async def periodic():
    while True:
        # Run the background task to fetch top artists
        async with Session.session() as session:
            asyncio.create_task(fetch_top_artists(session))

        # Schedule the task to run every hour
        now = datetime.utcnow()
        next_hour = (now + timedelta(hours=1)).replace(microsecond=0, second=0, minute=0)
        wait_seconds = (next_hour - now).total_seconds()
        print('started')
        await asyncio.sleep(wait_seconds)


async def init_models():
    ...
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        # await conn.run_sync(Base.metadata.drop_all)


@app.on_event("startup")
async def startup():
    ...
    await init_models()
    asyncio.create_task(periodic())


@app.on_event("shutdown")
async def shutdown():
    ...
