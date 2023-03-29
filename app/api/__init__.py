from fastapi import FastAPI

from app.api.healthcheck.routers import router as healthcheck_router
from app.api.artists.routers import router as artists_router


def init_routers(app: FastAPI) -> None:
    app.include_router(healthcheck_router, tags=["healthcheck"])
    app.include_router(artists_router, tags=["artists"])

