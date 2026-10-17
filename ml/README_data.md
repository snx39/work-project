# Dataset README（组员A）

本目录数据由 `ml/generate_data.py` 和 `ml/data_pipeline.py` 生成，并用 **DVC** 做版本化管理。

## 数据版本

### v1_house.csv（原始数据集，baseline 用）
- 样本数：200
- 真实房价关系含**非线性交互项** `area * bedrooms`（面积与卧室数共同影响价格）
- 含脏数据：少量负面积异常、极端离群价格 —— 用于体现"原始数据需清洗"
- DVC md5：`20422bb2ac631e08201e22396f1b281e`

### v2_house.csv（清洗 + 扩充，improved 用）
- 样本数：483
- 由 v1 清洗而来：剔除负面积、负价格、>99% 分位极端离群
- 补充 300 条干净合成样本（沿用同一真实关系，噪声更小）
- DVC md5：`81694c0110f38e52c9cd2c04ce4896c4`

## 生成方式

```bash
python ml/generate_data.py   # 生成 data/v1_house.csv
python ml/data_pipeline.py   # 生成 data/v2_house.csv
```

## DVC 版本化

```bash
dvc add data/v1_house.csv data/v2_house.csv   # 生成/更新 .dvc 指针
dvc push                                       # 推送数据对象到远程
```

- 指针文件 `data/v1_house.csv.dvc`、`data/v2_house.csv.dvc` 提交进 git；
- 原始 csv 由 `.gitignore` 排除（`data/*.csv`），不直接进 git。
