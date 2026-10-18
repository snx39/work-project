# Current Production Model Info

- Model artifact：`ml/model.pkl`
- Experiment run：Improved RandomForestRegressor（Run3，4 特征）
- MLflow run_id：`5348806125704019b9523c6c45c59d40`（以本地重跑为准）
- Dataset used：`data/v3_house.csv`（4 特征）
- DVC dataset pointer：`data/v3_house.csv.dvc`（md5 `23eb87254c1068a88c7f952566edb154`）
- Git commit hash：待合并到 dev 后更新为对应 commit

## 输入特征契约（对组员B 重要）
模型 `ml/model.pkl` 的输入特征为 **四个字段（顺序必须一致）**：
1. `area`（面积，float）
2. `bedrooms`（卧室数，int）
3. `bathrooms`（卫生间数，int）
4. `year_built`（建造年份，int）

预测输出为 `price`（float）。

> ⚠️ 组员B 的 `app/schemas.py` / `app/main.py` 必须与上述**完全一致**（4 个字段、顺序相同）。
> 推理时用带列名的 DataFrame：`["area","bedrooms","bathrooms","year_built"]`。
> 顺序/名称不同会导致 `predict()` 报错或结果错误。若 B 需扩展字段，先与组员A 同步并重新训练。
