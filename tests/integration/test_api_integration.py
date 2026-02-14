import pytest
from httpx import AsyncClient


async def get_app():
    from app.main import app

    return app


@pytest.mark.asyncio
async def test_health_check():
    """Test the health check endpoint."""
    app = await get_app()
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/ping")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"


@pytest.mark.asyncio
async def test_root_endpoint():
    """Test the root endpoint."""
    app = await get_app()
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "docs" in data
