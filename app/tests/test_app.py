import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


@pytest.mark.parametrize("payload", [
    {"area": 100.0, "bedrooms": 3, "bathrooms": 2, "year_built": 2010},
    {"area": 0.1, "bedrooms": 1, "bathrooms": 1, "year_built": 1900},
    {"area": 1000.0, "bedrooms": 10, "bathrooms": 8, "year_built": 2024},
])
def test_predict_valid(payload):
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    assert "predicted_price" in response.json()


@pytest.mark.parametrize("payload", [
    {"bedrooms": 3, "bathrooms": 2, "year_built": 2010},
    {"area": 100.0, "bathrooms": 2, "year_built": 2010},
    {"area": 100.0, "bedrooms": 3, "year_built": 2010},
    {"area": 100.0, "bedrooms": 3, "bathrooms": 2},
    {},
])
def test_predict_missing_field(payload):
    response = client.post("/predict", json=payload)
    assert response.status_code == 422