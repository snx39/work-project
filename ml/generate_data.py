# ml/generate_data.py
# 组员A：生成 v1 基础数据集（raw baseline，2 特征）与 v3 升级数据集（4 特征，对齐后端契约）
# 设计说明：
#   - v1：真实房价关系含"非线性交互项" area*bedrooms，线性模型无法拟合 -> 作为 baseline 合理欠拟合。
#   - v3：升级到 4 特征（area, bedrooms, bathrooms, year_built），且新特征真实影响价格，
#         用于与 B 的 app/schemas.py 四字段契约对齐后重新训练生产模型。
import os

import numpy as np
import pandas as pd


def generate_v1_dataset(save_path: str = "data/v1_house.csv") -> pd.DataFrame:
    """v1 原始数据集：含非线性交互 + 噪声 + 异常值（baseline 欠拟合，历史版本，保留）"""
    np.random.seed(42)
    n_samples = 200
    area = np.random.normal(loc=120, scale=30, size=n_samples)
    bedrooms = np.random.randint(1, 6, size=n_samples)
    price = (300 * area + 8000 * bedrooms + 60 * area * bedrooms
             + np.random.normal(0, 30000, n_samples))
    area[:10] = -np.abs(area[:10])
    price[-5:] += np.random.normal(0, 200000, 5)

    df = pd.DataFrame({
        "area": area.round(2),
        "bedrooms": bedrooms,
        "price": price.round(2),
    })
    os.makedirs(os.path.dirname(save_path) or ".", exist_ok=True)
    df.to_csv(save_path, index=False)
    print(f"Generated v1 dataset -> {save_path}, shape: {df.shape}")
    return df


def generate_v3_dataset(save_path: str = "data/v3_house.csv") -> pd.DataFrame:
    """v3 升级数据集：4 特征（area, bedrooms, bathrooms, year_built）且新特征真实影响价格。
    与 B 的 app/schemas.py 四字段契约完全对齐（特征名、顺序一致）。"""
    np.random.seed(42)
    n_samples = 400
    area = np.random.normal(loc=120, scale=30, size=n_samples)
    bedrooms = np.random.randint(1, 6, size=n_samples)
    bathrooms = np.random.randint(1, 5, size=n_samples)
    year_built = np.random.randint(1960, 2026, size=n_samples)
    price = (300 * area + 8000 * bedrooms + 60 * area * bedrooms
             + 20000 * bathrooms + 300 * (year_built - 1960)
             + np.random.normal(0, 30000, n_samples))

    df = pd.DataFrame({
        "area": area.round(2),
        "bedrooms": bedrooms,
        "bathrooms": bathrooms,
        "year_built": year_built,
        "price": price.round(2),
    })
    os.makedirs(os.path.dirname(save_path) or ".", exist_ok=True)
    df.to_csv(save_path, index=False)
    print(f"Generated v3 dataset -> {save_path}, shape: {df.shape}")
    return df


if __name__ == "__main__":
    generate_v1_dataset()
    generate_v3_dataset()
