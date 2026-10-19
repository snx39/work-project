# ml/train.py
# 组员A：训练房价回归模型 + MLflow 记录，固定保存 ml/model.pkl
# 用法：
#   python ml/train.py --dataset data/v3_house.csv --model-type rf --n-estimators 200  # 生产（4特征）
#   （历史 baseline：--dataset data/v1_house.csv --model-type linear）
import argparse
import os
import pickle
import subprocess

import mlflow
import mlflow.sklearn
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

# 模型输入特征 —— 必须与组员B的 app/schemas.py 字段完全一致！
# v3 起升级为 4 特征：area, bedrooms, bathrooms, year_built
FEATURES = ["area", "bedrooms", "bathrooms", "year_built"]
TARGET = "price"
MODEL_PATH = "ml/model.pkl"


def get_git_commit_hash() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"]).decode("ascii").strip()
    except (subprocess.CalledProcessError, FileNotFoundError, UnicodeDecodeError):
        return "unknown_git_hash"


def main(dataset_path: str, model_save_path: str, model_type: str,
         n_estimators: int = 200, max_depth: int | None = None) -> None:
    df = pd.read_csv(dataset_path)
    X = df[FEATURES]
    y = df[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    git_sha = get_git_commit_hash()

    mlflow.set_experiment("house_price_prediction")
    with mlflow.start_run():
        mlflow.log_param("git_commit_sha", git_sha)
        mlflow.log_param("dataset_path", dataset_path)
        mlflow.log_param("model_type", model_type)
        mlflow.log_param("features", FEATURES)
        mlflow.log_param("test_size", 0.2)
        mlflow.log_param("random_state", 42)

        if model_type == "linear":
            model = LinearRegression()
        elif model_type == "rf":
            model = RandomForestRegressor(
                n_estimators=n_estimators, max_depth=max_depth, random_state=42)
            mlflow.log_param("n_estimators", n_estimators)
            mlflow.log_param("max_depth", max_depth)
        else:
            raise ValueError("model_type only support linear / rf")

        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        mse = mean_squared_error(y_test, y_pred)
        rmse = float(np.sqrt(mse))
        r2 = r2_score(y_test, y_pred)
        mlflow.log_metric("mse", mse)
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("r2_score", r2)

        os.makedirs(os.path.dirname(model_save_path), exist_ok=True)
        with open(model_save_path, "wb") as f:
            pickle.dump(model, f)

        mlflow.log_artifact(model_save_path)
        mlflow.sklearn.log_model(
            model, "sklearn_model",
            skops_trusted_types=["sklearn.tree._tree.Tree"])

        run_id = mlflow.active_run().info.run_id
        print("=" * 50)
        print(f"Dataset: {dataset_path}")
        print(f"Model: {model_type}")
        print(f"Features: {FEATURES}")
        print(f"MSE = {mse:.2f} | RMSE = {rmse:.2f} | R2 = {r2:.4f}")
        print(f"Model saved -> {model_save_path}")
        print(f"MLflow run_id: {run_id}")
        print("=" * 50)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type=str, required=True, help="csv数据集路径")
    parser.add_argument("--model-type", default="linear", help="linear / rf")
    parser.add_argument("--n-estimators", type=int, default=200, help="RF 树数量")
    parser.add_argument("--max-depth", type=int, default=None, help="RF 最大深度")
    args = parser.parse_args()

    main(
        dataset_path=args.dataset,
        model_save_path=MODEL_PATH,
        model_type=args.model_type,
        n_estimators=args.n_estimators,
        max_depth=args.max_depth,
    )
