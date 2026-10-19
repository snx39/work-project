import os
import pickle

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from .schemas import HouseFeatures, HousePredictResponse

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
def predict(house: HouseFeatures):
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


# 可视化操作页面：普通用户填表单、点按钮即可查看预测房价（不依赖外部前端框架）
PAGE_HTML = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>房价预测</title>
<style>
  * { box-sizing: border-box; }
  body { margin:0; min-height:100vh; display:flex; align-items:center; justify-content:center;
         background:#f0f2f5; font-family:system-ui,-apple-system,"Microsoft YaHei",sans-serif; padding:16px; }
  .card { width:100%; max-width:420px; background:#fff; border-radius:16px; padding:28px 24px;
          box-shadow:0 8px 30px rgba(0,0,0,.08); }
  h1 { font-size:20px; margin:0 0 4px; text-align:center; }
  .sub { font-size:13px; color:#888; text-align:center; margin-bottom:20px; }
  label { display:block; font-size:13px; color:#444; margin:14px 0 6px; }
  input { width:100%; padding:11px 12px; font-size:15px; border:1px solid #d9d9d9; border-radius:10px; }
  input:focus { outline:none; border-color:#1677ff; }
  button { width:100%; margin-top:20px; padding:13px; font-size:16px; color:#fff; background:#1677ff;
           border:none; border-radius:10px; cursor:pointer; }
  button:disabled { background:#9fc3ff; cursor:not-allowed; }
  .result { margin-top:20px; padding:18px; border-radius:12px; background:#e8f1ff; text-align:center; display:none; }
  .result .price { font-size:28px; font-weight:700; color:#1677ff; }
  .result .unit { font-size:14px; color:#555; }
  .error { margin-top:16px; padding:12px; border-radius:10px; background:#fff2f0; color:#cf1322;
           font-size:13px; display:none; white-space:pre-wrap; }
</style>
</head>
<body>
  <div class="card">
    <h1>房价预测</h1>
    <div class="sub">填写房屋信息，点击按钮查看预测价格</div>
    <label>面积（平方米，需大于0）</label>
    <input id="area" type="number" step="0.1" placeholder="例如 120" value="120">
    <label>卧室数量（1~20）</label>
    <input id="bedrooms" type="number" min="1" max="20" placeholder="例如 3" value="3">
    <label>卫生间数量（0~10）</label>
    <input id="bathrooms" type="number" min="0" max="10" placeholder="例如 2" value="2">
    <label>建造年份（1900~2026）</label>
    <input id="year_built" type="number" min="1900" max="2026" placeholder="例如 2000" value="2000">
    <button id="btn" onclick="predict()">开始预测</button>
    <div class="result" id="result">
      <div class="price" id="price"></div>
      <div class="unit">人民币元（CNY）</div>
    </div>
    <div class="error" id="error"></div>
  </div>
<script>
function val(id) { return document.getElementById(id).value; }
function predict() {
  var btn = document.getElementById("btn");
  var result = document.getElementById("result");
  var error = document.getElementById("error");
  result.style.display = "none";
  error.style.display = "none";
  btn.disabled = true;
  btn.textContent = "预测中...";
  var payload = {
    area: Number(val("area")),
    bedrooms: Number(val("bedrooms")),
    bathrooms: Number(val("bathrooms")),
    year_built: Number(val("year_built"))
  };
  fetch("/predict", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  })
  .then(function(resp) {
    return resp.json().then(function(data) { return { ok: resp.ok, data: data }; });
  })
  .then(function(r) {
    if (r.ok) {
      var n = Number(r.data.predicted_price);
      document.getElementById("price").textContent =
        n.toLocaleString("zh-CN", { maximumFractionDigits: 2 });
      result.style.display = "block";
    } else {
      var msgs = (r.data.detail || []).map(function(d) { return d.loc ? d.loc.join(".") + ": " + d.msg : d.msg; });
      error.textContent = "输入不合法：\\n" + msgs.join("\\n");
      error.style.display = "block";
    }
  })
  .catch(function() {
    error.textContent = "请求失败，请确认服务已启动";
    error.style.display = "block";
  })
  .finally(function() {
    btn.disabled = false;
    btn.textContent = "开始预测";
  });
}
</script>
</body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
def home_page():
    """可视化操作首页：表单 + 预测按钮，调用 /predict 返回结果"""
    return HTMLResponse(content=PAGE_HTML)


if __name__ == "__main__" :
    import uvicorn
    uvicorn.run(app,host = "0.0.0.0", port = 8000)

