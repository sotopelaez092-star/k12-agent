from fastapi.testclient import TestClient

from server.app.main import app

client = TestClient(app)


def test_ready_ok():
    r = client.get("/ready")
    assert r.status_code == 200
    assert r.json() == {"ready": True}


def test_ready_request_id_header():
    # 自动生成的 X-Request-ID 存在
    r = client.get("/ready")
    assert r.status_code == 200
    assert r.headers.get("X-Request-ID")

    # 传入的 X-Request-ID 会被回传（传播）
    rid = "test-rid-123"
    r2 = client.get("/ready", headers={"X-Request-ID": rid})
    assert r2.status_code == 200
    assert r2.headers.get("X-Request-ID") == rid
