from fastapi.testclient import TestClient
from server.app.main import app

client = TestClient(app)

def test_422_error_payload_and_header():
    # 触发类型校验错误：age 应为 int，这里传字符串
    r = client.post("/validate", json={"name": "Alice", "age": "bad"})
    assert r.status_code == 422
    data = r.json()
    assert data["error"]["code"] == 422
    assert data["error"]["message"] == "Validation Error"
    assert isinstance(data["error"]["details"], list) and len(data["error"]["details"]) >= 1
    # 响应头携带自动生成的 X-Request-ID
    assert r.headers.get("X-Request-ID")

def test_422_request_id_propagation():
    rid = "rid-422-xyz"
    r = client.post("/validate", json={"name": "Bob", "age": "oops"}, headers={"X-Request-ID": rid})
    assert r.status_code == 422
    assert r.headers.get("X-Request-ID") == rid