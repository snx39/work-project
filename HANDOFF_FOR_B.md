# 交接说明 —— 给组员B（后端 API 工程师）

> 组员A 的数据与模型部分已全部完成并合入 `dev` 分支。你接手后端推理时，按本说明操作即可。

## 一、项目结构（你只需要关心 app/ 和 ml/model.pkl）

```
ml-dvc-project/
├── app/                 # ← 你负责：main.py + schemas.py（现在为空，需你创建）
├── ml/
│   ├── model.pkl        # ← 已训练的模型，直接加载
│   ├── train.py         # 训练脚本（A 的，可参考但不改）
│   ├── generate_data.py # 数据生成（A 的）
│   ├── data_pipeline.py # 数据处理（A 的）
│   ├── README_data.md / README_experiments.md / PROVENANCE.md
│   └── registry/current_model.md   # 生产模型信息 + 特征契约
├── data/                # DVC 管理的数据（*.csv.dvc 指针；数据对象在 DVC 远程）
├── .dvc/                # DVC 配置
├── .gitignore
└── requirements.txt     # 由组员C 负责维护
```

## 二、模型契约（最重要 —— 你的 schemas.py 必须对齐）

`ml/model.pkl` 是一个 **RandomForestRegressor**，由 sklearn `pickle` 序列化。

| 项目 | 值 |
|------|----|
| 模型文件 | `ml/model.pkl` |
| 加载方式 | `pickle.load(open("ml/model.pkl","rb"))` |
| **输入特征（必须且仅这2个）** | `area`（float，面积）、`bedrooms`（int，卧室数） |
| 输出 | `price`（float，预测房价） |
| 底层类型 | `sklearn.ensemble.RandomForestRegressor` |

**加载代码示例（B 的 main.py 里用）**：
```python
import pickle
import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# 加载 A 的模型（放在启动时）
with open("ml/model.pkl", "rb") as f:
    model = pickle.load(f)

class HouseFeatures(BaseModel):
    area: float        # 面积
    bedrooms: int      # 卧室数

@app.post("/predict")
def predict(features: HouseFeatures):
    # 必须用带列名的 DataFrame，顺序一致，避免 sklearn 特征名告警
    import pandas as pd
    X = pd.DataFrame([{
        "area": features.area,
        "bedrooms": features.bedrooms,
    }])
    price = float(model.predict(X)[0])
    return {"predicted_price": price}
```

> ⚠️ **特征名必须精确为 `area`、`bedrooms`，顺序/名称不同会导致 `predict()` 报错或结果错误。**
> 若你要扩展字段（如 bathrooms/age），先找组员A 同步并重新训练，不能只改 schema。

## 三、如何拿到项目（二选一）

### 方式A（推荐）：git 克隆 dev 分支
```bash
git clone https://github.com/SNX39/work-project.git
git checkout dev          # 当前 A 的部分已在 dev（含 ml/model.pkl）
```
- `ml/model.pkl` 已在 dev 分支，克隆/切换后直接存在。
- 若提示仓库已迁移到 `https://github.com/snx39/work-project.git`（大小写），以该地址为准。

### 方式B：接收 A 打包的文件夹
- 解压后直接进入项目根目录使用。
- 确保 `ml/model.pkl` 存在（A 已放行并提交）。

## 四、运行环境
- Python 3.10+；需要依赖：`fastapi`、`uvicorn`、`pandas`、`scikit-learn`、`numpy`。
- `requirements.txt` 由组员C 维护（含 fastapi/uvicorn/scikit-learn/pandas/mlflow/dvc/ruff/pytest）。
- 建议创建虚拟环境：`python -m venv .venv && .venv\Scripts\activate && pip install -r requirements.txt`

## 五、可选的 Mock（若想先跑通接口再等模型）
模型已经就绪，不需要 Mock。如果为了先写接口逻辑，可临时返回固定值，最后把加载代码换成上面的 `model.predict(X)` 即可（接口逻辑不变）。

## 六、需要 DVC 数据吗？
后端推理**不需要** `data/*.csv`（模型已封装特征）。只有想复现训练或跑测试对比时才需：
```bash
dvc pull     # 拉取 v1/v2 数据（远程为本地 dvcstore；评分前 A 会配真实 Azure）
```

## 七、你的任务（分工摘要）
1. 编写 `app/schemas.py`：定义 `HouseFeatures`（area, bedrooms 及约束，如 area>0、1<=bedrooms<=10）。
2. 编写 `app/main.py`：实现 `/predict`，加载 `ml/model.pkl` 返回预测。
3. 在 `README.md` 补充 API 文档（如何调用 /predict、输入输出格式）。
4. 注意：从 `dev` 切自己的特性分支 `feature/backend-api`，完成后合并回 dev。

> 有任何模型契约疑问，先看 `ml/registry/current_model.md` 或直接问组员A。
