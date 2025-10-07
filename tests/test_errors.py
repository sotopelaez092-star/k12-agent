from fastapi.testclient import TestClient

from server.app.main import app

client = TestClient(app)


def test_404_error_payload():
    r = client.get("/not-exists")
    assert r.status_code == 404
    assert r.json() == {"error": {"code": 404, "message": "Not Found"}}
    assert r.headers.get("X-Request-ID")


def test_404_request_id_propagation():
    rid = "rid-404-abc"
    r = client.get("/not-exists", headers={"X-Request-ID": rid})
    assert r.status_code == 404
    assert r.headers.get("X-Request-ID") == rid


def test_405_error_payload():
    r = client.post("/health")
    assert r.status_code == 405
    assert r.json() == {"error": {"code": 405, "message": "Method Not Allowed"}}
    assert r.headers.get("X-Request-ID")


def test_405_request_id_propagation():
    rid = "rid-405-def"
    r = client.post("/health", headers={"X-Request-ID": rid})
    assert r.status_code == 405
    assert r.headers.get("X-Request-ID") == rid
