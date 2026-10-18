from fastapi import FastAPI,HTTPException
from .schemas import HouseFeature,HousePredictResponse
import pickle
import os

app = FastAPI(title="House Price Prediction MLOps Service")


MODEL_PATH = "ml/model.pkl"
use_mock_model: bool = False 

# Mock模型函数
def mock_predict(features: HouseFeatures) -> float:
    """模拟预测，周靖凯未交付模型使用，接口行为保持不变"""
    base_price = features.area * 8000 + features.bedrooms * 20000
    return round(base_price,2)

# 真实模型加载
real_model = None
if not use_mock_model:
    if os.path.exists(MODEL_PATH):
        with open(MODEL_PATH,"rb") as f:
            real_model = pickle.load(f)
    else:
        raise RuntimeError(f"模型文件 {MODEL_PATH} 不存在，请等待周靖凯提交模型")


@app.post("/predict",response_model = HousePredictResponse)
def predict(house: HouseFeature):
    """房价预测接口"""
    if use_mock_model:
        pred = mock_predict(house)
    else:
        input_data = [
            [house.area, house.bedrooms, house.bathrooms, house.year_built]
        ]
        pred = real_model.predict(input_data)[0]

    return HousePredictResponse(predicted_price = float(pred))

@app.get("/health")
def health_check():
    """健康检查口，CI/Docker启动检测用（高子腾的测试需要）"""
    return {"status":"ok","mock_mode": use_mock_model}

if __name__ == "__main__" :
    import uvicorn
    uvicorn.run(app,host = "0.0.0.0", port = 8000)

