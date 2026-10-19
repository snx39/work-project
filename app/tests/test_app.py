import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


# 1. 正常与边界值测试
@pytest.mark.parametrize("payload", [
    {"area": 100.0, "bedrooms": 3, "bathrooms": 2, "year_built": 2010},
    {"area": 0.1, "bedrooms": 1, "bathrooms": 1, "year_built": 1900}, # 极小边界
    {"area": 1000.0, "bedrooms": 10, "bathrooms": 8, "year_built": 2024}, # 极大边界
])
def test_predict_valid(payload):
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    assert "predicted_price" in response.json()


# 2. 缺失字段测试
@pytest.mark.parametrize("payload", [
    {"bedrooms": 3, "bathrooms": 2, "year_built": 2010},
    {"area": 100.0, "bathrooms": 2, "year_built": 2010},
    {},
])
def test_predict_missing_field(payload):
    response = client.post("/predict", json=payload)
    assert response.status_code == 422


# 3. 非法输入测试 (负数、超长字符串等)
@pytest.mark.parametrize("payload", [
    {"area": -50.0, "bedrooms": 3, "bathrooms": 2, "year_built": 2010}, # 负数面积
    {"area": 100.0, "bedrooms": 50, "bathrooms": 2, "year_built": 2010}, # 离谱的卧室数
    {"area": 100.0, "bedrooms": 3, "bathrooms": 2, "year_built": 3000}, # 未来年份
])
def test_predict_invalid_input(payload):
    response = client.post("/predict", json=payload)
    # 期望被拦截（返回 422）
    assert response.status_code == 422