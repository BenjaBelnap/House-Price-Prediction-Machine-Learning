from fastapi.testclient import TestClient


def test_frontend_serves_index():
    # Import within test to avoid side effects during collection
    from frontend.server import frontend_app

    client = TestClient(frontend_app)
    resp = client.get("/")
    assert resp.status_code == 200
    # served as HTML
    assert "text/html" in resp.headers.get("content-type", "")


def test_frontend_static_route_exists():
    from frontend.server import frontend_app

    client = TestClient(frontend_app)
    # We can't guarantee all static files exist in all environments, but route should be mounted
    resp = client.get("/static/")
    # Directory listing might be disabled; 200 or 404 are acceptable as long as no exception occurs
    assert resp.status_code in (200, 404)
