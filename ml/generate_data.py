# ml/generate_data.py
import pandas as pd
import numpy as np
import os

def generate_v1_dataset(save_path: str = "data/v1_house.csv"):
    """v1 原始数据集，包含异常值（负数面积）"""
    np.random.seed(42)
    n_samples = 200
    area = np.random.normal(loc=120, scale=30, size=n_samples)
    bedrooms = np.random.randint(1, 6, size=n_samples)
    # 人为制造异常：部分面积为负数
    area[:10] = -np.abs(area[:10])
    price = area * 1200 + bedrooms * 15000 + np.random.normal(0, 8000, n_samples)

    df = pd.DataFrame({
        "area": area,
        "bedrooms": bedrooms,
        "price": price
    })
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    df.to_csv(save_path, index=False)
    print(f"Generated v1 dataset -> {save_path}, shape: {df.shape}")
    return df


def generate_v2_dataset(v1_path: str = "data/v1_house.csv", save_path: str = "data/v2_house.csv"):
    """
    v2改进数据集：
    1. 删除area负数异常样本
    2. 新增30条合成样本
    """
    df = pd.read_csv(v1_path)
    # 移除异常值
    df_clean = df[df["area"] > 0].copy()
    # 增加合成样本
    np.random.seed(42)
    n_new = 30
    area_new = np.random.normal(loc=150, scale=20, size=n_new)
    bedrooms_new = np.random.randint(2, 5, size=n_new)
    price_new = area_new * 1200 + bedrooms_new * 15000 + np.random.normal(0, 6000, n_new)
    df_new = pd.DataFrame({
        "area": area_new,
        "bedrooms": bedrooms_new,
        "price": price_new
    })
    df_v2 = pd.concat([df_clean, df_new], ignore_index=True)
    df_v2.to_csv(save_path, index=False)
    print(f"Generated v2 dataset -> {save_path}, shape: {df_v2.shape}")
    return df_v2


if __name__ == "__main__":
    generate_v1_dataset()
    generate_v2_dataset()
