from fastapi.testclient import TestClient

from car_sharing import app
from routers.cars import add_car
from schemas import CarInput, Car


client = TestClient(app)


def test_add_car():
    response = client.post("/api/cars/", json={
        "doors": 7, "size": "xxl"}, headers={}
    )
    assert response.status_code == 200
    car = response.json()
    assert car['doors'] == 7
    assert car['size'] == 'xxl'
