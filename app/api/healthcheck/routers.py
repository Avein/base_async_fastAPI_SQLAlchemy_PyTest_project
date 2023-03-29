from fastapi import APIRouter
from loguru import logger
from starlette import status

from app.api.healthcheck.schemas import HealthcheckSchema

router = APIRouter()


@router.get(
    "/healthcheck",
    response_model=HealthcheckSchema,
    status_code=status.HTTP_200_OK
)
async def healthcheck() -> HealthcheckSchema:
    logger.info("Healthcheck OK")
    logger.error("Healthcheck OK")
    logger.debug("Healthcheck OK")

    return HealthcheckSchema(status='OK')
