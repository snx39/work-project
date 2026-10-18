# ML DevOps Project

## 1. API 文档
- `POST /predict`
  - Request JSON: `{"area": 100.0, "bedrooms": 2}`
  - Response: `{"predicted_price": 150.0}` (200 OK)
  - 缺失字段或类型错误返回 422。

## 2. CI/CD 工作流
本项目采用标准分支策略：
- 开发者在 `feature/*` 分支开发。
- **PR 触发 CI**：任何向 `dev`、`staging`、`main` 的 PR 都会触发 GitHub Actions，执行 Ruff 格式检查、Pytest 单元测试、Docker 构建测试。
- **Staging 部署**：合并到 `staging` 分支时，自动注入 Staging 环境变量并构建镜像。
- **Production 部署**：合并到 `main` 分支时，自动注入生产环境变量并构建镜像。