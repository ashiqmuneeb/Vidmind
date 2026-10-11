import pytest
from httpx import AsyncClient, ASGITransport
from backend.app.main import app
from backend.app.db.database import init_db


@pytest.fixture(autouse=True)
async def initialize_database():
    await init_db()


@pytest.fixture
async def async_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        yield client
