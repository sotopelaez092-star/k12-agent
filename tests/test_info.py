from fastapi.testclient import TestClient
from server.app.main import app

client = TestClient(app)

def test_info_ok():
    r = client.get("/info")
    assert r.status_code == 200
    data = r.json()
    assert set(["app_name", "version", "env", "startup_time"]).issubset(set(data.keys()))
    assert isinstance(data["app_name"], str)
    assert isinstance(data["version"], str)
    assert isinstance(data["env"], str)
    assert isinstance(data["startup_time"], str)

def test_info_request_id_header():
    # 传入的 X-Request-ID 会被回传
    rid = "info-rid-456"
    r = client.get("/info", headers={"X-Request-ID": rid})
    assert r.status_code == 200
    assert r.headers.get("X-Request-ID") == rid