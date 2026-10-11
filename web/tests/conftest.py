import pytest
from httpx2 import AsyncClient

WEB_URL = "http://localhost:8080"
API_URL = "http://localhost:8000"


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture
async def web_client():
    async with AsyncClient(base_url=WEB_URL) as client:
        yield client


@pytest.fixture
async def api_client():
    async with AsyncClient(base_url=API_URL) as client:
        yield client


@pytest.fixture
async def api_entry(api_client):
    response = await api_client.post(
        "/entries",
        json={
            "provider": "web-test",
            "payload": {
                "title": "original title",
                "description": "original description",
            },
        },
    )
    response.raise_for_status()
    return response.json()
