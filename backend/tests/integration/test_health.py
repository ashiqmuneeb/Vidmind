import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health_endpoint(async_client: AsyncClient):
    response = await async_client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["database"] == "connected"
    assert "hardware" in data
    assert "profile" in data["hardware"]
    assert "cpu_logical_cores" in data["hardware"]
    assert data["hardware"]["cpu_logical_cores"] >= 1


@pytest.mark.asyncio
async def test_root_endpoint(async_client: AsyncClient):
    response = await async_client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["app"] == "VidMind"
    assert "/docs" in data["docs"]
