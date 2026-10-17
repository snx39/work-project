# MLflow Experiments Summary

Experiment `house_price_prediction` 下记录两次实验（本地 MLflow backend，`mlruns/`）。

## Run1: Baseline Model
- Dataset：`data/v1_house.csv`（含脏数据/异常）
- Model：LinearRegression
- Metrics：
  - MSE：987951712.85
  - RMSE：31431.70
  - R2：0.3364
- MLflow run_id：`609388a8581f41da9d3a81e2a1d3feab`
- Purpose：baseline 参考性能

## Run2: Improved Production Model
- Dataset：`data/v2_house.csv`（清洗 + 扩充）
- Model：RandomForestRegressor（n_estimators=200）
- Metrics：
  - MSE：587830954.34
  - RMSE：24245.23
  - R2：0.3995
- MLflow run_id：`7f677c570f0247b2bd4694280ed202eb`

## Production Selection

选择 **Run2（RF + v2）** 为生产模型。

**理由**：
- v2 数据更干净（剔除异常/离群、补充合成样本）；
- 真实房价关系含非线性交互项 `area*bedrooms`，随机森林可拟合非线性，而线性 baseline 无法拟合；
- 因此 Run2 的 MSE 由 987.9M 降至 587.8M（降约 **40%**）、RMSE 由 31431 降至 24245、R2 由 0.3364 升至 **0.3995**，全面优于 Run1。

**优化指标**：RMSE（回归任务常用，量纲与价格一致、可解释）。

> 注：此处指标为真实复现结果，与 `mlruns/` 中两个 run 的 `mse / rmse / r2_score` 一致。
