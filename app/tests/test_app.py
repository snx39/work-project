from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_predict_normal():
    response = client.post("/predict", json={"area": 100.0, "bedrooms": 2})
    assert response.status_code == 200
    assert "predicted_price" in response.json()


def test_predict_boundary_small():
    response = client.post("/predict", json={"area": 0.1, "bedrooms": 1})
    assert response.status_code == 200


def test_predict_missing_field():
    response = client.post("/predict", json={"area": 100.0})
    assert response.status_code == 422