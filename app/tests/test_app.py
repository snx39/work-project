import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


@pytest.mark.parametrize("payload", [
    {"area": 100.0, "bedrooms": 2},
    {"area": 50.0, "bedrooms": 1},
    {"area": 200.0, "bedrooms": 4},
])
def test_predict_valid(payload):
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    assert "predicted_price" in response.json()


@pytest.mark.parametrize("payload", [
    {"area": 0.1, "bedrooms": 1},
    {"area": 1000.0, "bedrooms": 10},
])
def test_predict_boundary(payload):
    response = client.post("/predict", json=payload)
    assert response.status_code == 200


@pytest.mark.parametrize("payload", [
    {"area": 100.0},  # 缺 bedrooms
    {"bedrooms": 2},  # 缺 area
    {},               # 全缺
])
def test_predict_missing_field(payload):
    response = client.post("/predict", json=payload)
    assert response.status_code == 422