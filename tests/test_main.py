from fastapi.testclient import TestClient

from api.main import app


client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == ["Hello, world!"]

def test_version():
    response = client.get("/version")

    assert response.status_code == 200
    assert response.json() == {"version": "test"}