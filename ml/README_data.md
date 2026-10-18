# Dataset README（组员A）

本目录数据由 `ml/generate_data.py` 和 `ml/data_pipeline.py` 生成，并用 **DVC** 做版本化管理。

## 数据版本

### v1_house.csv（原始数据集，baseline 用，2 特征）
- 样本数：200
- 真实房价关系含**非线性交互项** `area * bedrooms`
- 含脏数据：负面积异常、极端离群价格
- DVC md5：`20422bb2ac631e08201e22396f1b281e`

### v2_house.csv（清洗 + 扩充，improved 用，2 特征）
- 样本数：483
- 由 v1 清洗：剔除负面积、负价格、>99% 分位极端离群；补充 300 条干净合成样本
- DVC md5：`81694c0110f38e52c9cd2c04ce4896c4`

### v3_house.csv（当前生产数据集，4 特征，对齐后端契约）
- 样本数：400
- 由 `ml/generate_data.py::generate_v3_dataset()` 生成
- **新增特征**：`bathrooms`（卫生间数）、`year_built`（建造年份），且两者真实影响价格
- 特征与 B 的 `app/schemas.py` 契约对齐：`area, bedrooms, bathrooms, year_built`
- DVC md5：`23eb87254c1068a88c7f952566edb154`

## 生成方式

```bash
python ml/generate_data.py   # 生成 data/v1_house.csv 与 data/v3_house.csv
python ml/data_pipeline.py   # 由 v1 生成 v2（历史版本）
```

## DVC 版本化

```bash
dvc add data/v1_house.csv data/v2_house.csv data/v3_house.csv
dvc push
```

- 指针文件提交进 git；原始 csv 由 `.gitignore` 排除（`data/*.csv`）。
