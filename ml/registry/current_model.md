# Current Production Model Info

- Model artifact：`ml/model.pkl`
- Experiment run：Improved RandomForestRegressor（Run2）
- MLflow run_id：`7f677c570f0247b2bd4694280ed202eb`
- Dataset used：`data/v2_house.csv`（清洗 + 扩充）
- DVC dataset pointer：`data/v2_house.csv.dvc`（md5 `81694c0110f38e52c9cd2c04ce4896c4`）
- Git commit hash：`1e7cbf7e963644e027e471af511aef3c38238ec1`

## 输入特征契约（对组员B 重要）
模型 `ml/model.pkl` 的输入特征为 **两个字段**：
- `area`（面积，float）
- `bedrooms`（卧室数，int）

预测输出为 `price`（float）。

> ⚠️ 组员B 的 `app/schemas.py` 中 `HouseFeatures` 字段**必须与上述完全一致**（`area`, `bedrooms`），
> 顺序/名称不同会导致 `predict()` 报错或结果错误。若 B 需要扩展字段，需先与组员A 同步并重新训练。
