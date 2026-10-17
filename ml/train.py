# ml/train.py
import mlflow
import mlflow.sklearn
import pandas as pd
import pickle
import argparse
import subprocess
import os
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score


def get_git_commit_hash() -> str:
    """获取当前git commit SHA，记录进mlflow参数"""
    try:
        return subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode('ascii').strip()
    except Exception:
        return "unknown_git_hash"


def main(dataset_path: str, model_save_path: str, model_type: str):
    # 读取数据集
    df = pd.read_csv(dataset_path)
    X = df[["area", "bedrooms"]]
    y = df["price"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    git_sha = get_git_commit_hash()

    # 设置MLflow实验名称
    mlflow.set_experiment("house_price_prediction")

    with mlflow.start_run():
        # ---------- 记录参数 log_param ----------
        mlflow.log_param("git_commit_sha", git_sha)
        mlflow.log_param("dataset_path", dataset_path)
        mlflow.log_param("model_type", model_type)
        mlflow.log_param("test_size", 0.2)
        mlflow.log_param("random_state", 42)

        # 选择模型
        if model_type == "linear":
            model = LinearRegression()
        elif model_type == "rf":
            model = RandomForestRegressor(n_estimators=50, random_state=42)
            mlflow.log_param("n_estimators", 50)
        else:
            raise ValueError("model_type only support linear / rf")

        # 训练
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        # ---------- 计算指标 log_metric ----------
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        mlflow.log_metric("mse", mse)
        mlflow.log_metric("r2_score", r2)

        # ---------- 保存本地模型文件（给组员B后端使用） ----------
        os.makedirs(os.path.dirname(model_save_path), exist_ok=True)
        with open(model_save_path, "wb") as f:
            pickle.dump(model, f)

        # ---------- MLflow记录artifact ----------
        mlflow.log_artifact(model_save_path)

        print("="*50)
        print(f"Dataset: {dataset_path}")
        print(f"Model: {model_type}")
        print(f"MSE = {mse:.2f}")
        print(f"R2 score = {r2:.4f}")
        print(f"Model saved -> {model_save_path}")
        print("="*50)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type=str, required=True, help="csv数据集路径")
    parser.add_argument("--model-type", default="linear", help="linear / rf")
    args = parser.parse_args()

    main(
        dataset_path=args.dataset,
        model_save_path="ml/model.pkl",
        model_type=args.model_type
    )
