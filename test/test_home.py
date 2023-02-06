from fastapi.testclient import TestClient

from car_sharing import app

client = TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert "Welcome" in response.text
