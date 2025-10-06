from server.app.main import app
from httpx import AsyncClient, ASGITransport

import pytest

@pytest.mark.asyncio
async def test_health_integration():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.get("/health")
        assert resp.status_code == 200
        assert resp.json() == {"status": "ok"}
