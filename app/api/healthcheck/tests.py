import pytest
from httpx import AsyncClient
from app.tests.conftest import async_client  # noqa: F401


@pytest.mark.asyncio
async def test_health(async_client: AsyncClient) -> None:
    response = await async_client.get(
        "http://0.0.0.0:8000/healthcheck",
    )
    assert 200 == response.status_code
    assert response.json() == {"status": "OK"}
