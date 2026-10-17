\# PROVENANCE

Model training provenance record:

1\. Training dataset: v2\_house.csv, tracked \& versioned by DVC.

2\. Training entry script: ml/train.py

3\. Experiment tracking: MLflow local backend, artifacts stored in ./mlruns (not committed to git).

4\. Output model artifact: ml/model.pkl — 通过 git 提交到 dev 分支，供后端组员B的推理 API 加载（已用 `!ml/model.pkl` 从 .gitignore 放行）。

5\. DVC remote: local folder remote (`C:\Users\29518\Desktop\dvcstore`) simulating Azure blob storage for coursework.

> ⚠️ 交付注意：评分要求 **MS Azure remote**。当前用本地文件夹 remote 模拟，仅作课程演示。
> 提交/评分前应将 remote 替换为真实 Azure Blob Storage：
> ```bash
> dvc remote add -d azure_storage azure://<container>/<prefix>
> dvc remote modify azure_storage connection_string "<SAS_or_connection_string>"
> dvc push
> ```
> 需具备 Azure 账号与容器凭据后再执行。



