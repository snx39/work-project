# House Price Prediction — MLOps / DevOps Project

基于 Scikit-learn 的房价预测服务，完整集成 Git 分支管理、FastAPI 后端、pytest 测试、Ruff  lint、Docker 打包与 GitHub Actions CI/CD，并用 DVC 做数据版本、MLflow 做实验跟踪。

## 1. 本地运行

```bash
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

服务启动后访问 `http://localhost:8000/docs` 查看交互式接口。

## 2. API 文档

### 健康检查

`GET /health`

返回服务状态，用于 CI 与容器启动探测。

```json
{ "status": "ok", "mock_mode": false }
```

### 房价预测

`POST /predict`

请求体（4 个字段，均为必填，含取值约束）：

```json
{
  "area": 100.0,
  "bedrooms": 3,
  "bathrooms": 2,
  "year_built": 2010
}
```

| 字段 | 类型 | 约束 |
| --- | --- | --- |
| `area` | float | 房屋面积，必须大于 0（平方米） |
| `bedrooms` | int | 卧室数量，1 ~ 20 |
| `bathrooms` | int | 卫生间数量，0 ~ 10 |
| `year_built` | int | 建造年份，1900 ~ 2026 |

成功响应（200）：

```json
{ "predicted_price": 157444.25, "unit": "CNY" }
```

缺失字段、类型错误或取值越界（负数、超范围、未来年份等）返回 `422 Unprocessable Entity`。

## 3. CI/CD 工作流与分支策略

分支链路：`feature/* → dev → staging → main`。

- **PR 门禁（pull_request 到 dev / staging / main）**：触发 GitHub Actions，依次执行
  1. 安装依赖 `pip install -r requirements.txt`
  2. Ruff 静态检查 `ruff check .`
  3. pytest 测试 `pytest app/tests/ -v`
  4. 构建 Docker 镜像确认无构建错误
  - CI 失败的 PR 不允许合并。
- **Staging（push 到 staging）**：注入 `STAGING_ENV` Secret 生成 `.env`，构建 Staging 镜像。
- **Production（push 到 main）**：注入 `PROD_ENV` Secret 生成 `.env`，构建 Production 镜像。

```
feature/*  --PR(ruff/pytest/docker)-->  dev  --merge-->  staging  --merge-->  main
                                            |                |                |
                                            |            构建Staging镜像     构建Prod镜像
                                            +---------- CI 门禁检查 ---------+
```

## 4. 仓库结构

```
.
├── app/
│   ├── main.py          # FastAPI 入口与 /predict、/health
│   ├── schemas.py       # Pydantic 请求/响应模型
│   └── tests/          # pytest 测试（正常/缺字段/非法输入）
├── ml/
│   ├── train.py         # 训练脚本（MLflow 记录参数/指标/模型）
│   ├── model.pkl        # 生产模型
│   ├── README_data.md       # 数据版本 v1/v2 说明
│   └── README_experiments.md# 实验对比与生产模型选择
├── data/                # DVC 管理的数据（仅 .dvc 指针入库）
├── .github/workflows/ci.yml
├── Dockerfile
├── .dockerignore
├── DEPLOYMENT.md
└── requirements.txt
```

## 5. MLOps 说明

- **数据版本（DVC）**：训练数据用 DVC 跟踪，仓库仅保存 `.dvc` 指针，原始数据不提交到 Git。
- **实验跟踪（MLflow）**：每次训练记录 git commit、数据集版本、超参数、指标与模型产物；基线模型与改进模型至少两个实验，生产模型见 `ml/README_experiments.md`。
