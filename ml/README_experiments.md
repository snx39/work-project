# MLflow Experiments Summary

Experiment `house_price_prediction` 下记录实验（本地 MLflow backend，`mlruns/`）。

## Run1: Baseline Model（历史，2 特征）
- Dataset：`data/v1_house.csv`（含脏数据/异常）
- Model：LinearRegression
- Metrics：MSE 987951712.85 | RMSE 31431.70 | R2 0.3364
- MLflow run_id：`609388a8581f41da9d3a81e2a1d3feab`
- Purpose：baseline 参考性能

## Run2: Improved Model（历史，2 特征）
- Dataset：`data/v2_house.csv`（清洗 + 扩充）
- Model：RandomForestRegressor（n_estimators=200）
- Metrics：MSE 587830954.34 | RMSE 24245.23 | R2 0.3995
- MLflow run_id：`7f677c570f0247b2bd4694280ed202eb`

## Run3: 当前生产模型（4 特征）
- Dataset：`data/v3_house.csv`（area, bedrooms, bathrooms, year_built）
- Model：RandomForestRegressor（n_estimators=200）
- Metrics：MSE 818819129.83 | RMSE 28615.02 | R2 0.5037
- MLflow run_id：`5348806125704019b9523c6c45c59d40`（以本地重跑为准）
- Purpose：与 B 后端四字段契约对齐，作为当前生产模型

## Production Selection

选择 **Run3（RF + v3，4 特征）** 为生产模型。

**理由**：
- 特征升级到 4 个，加入 `bathrooms` / `year_built` 后信息更丰富；
- R2 由 Run2 的 0.3995 提升至 0.5037（解释力显著增强）；
- 4 特征与 B 的 API 契约完全对齐，避免推理维度不匹配。

**优化指标**：R2（回归解释力）+ RMSE（量纲与价格一致、可解释）。
注：不同数据集分布不同，RMSE 绝对值跨版本不可直接横比；以同分布内的 R2 相对提升为准。
