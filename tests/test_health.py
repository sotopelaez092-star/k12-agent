from fastapi.testclient import TestClient

from server.app.main import app


def test_health():
    c = TestClient(app)
    assert c.get("/health").json() == {"status": "ok"}
