# ml/generate_data.py
# 组员A：生成 v1 基础数据集（raw baseline）
# 设计说明：
#   - 真实房价关系包含"非线性交互项" area * bedrooms（面积与卧室数的交互影响价格），
#     线性模型(LinearRegression)无法拟合这种交互，因此作为 baseline 会合理欠拟合。
#   - 人为加入两类"脏数据"：少量负面积异常、少量极端离群价格。
#     目的：让 v1 是"未清理的原始数据"，体现 v2 通过清理+扩充能明显提升。
import os
import numpy as np
import pandas as pd


def generate_v1_dataset(save_path: str = "data/v1_house.csv") -> pd.DataFrame:
    """v1 原始数据集：含非线性交互 + 噪声 + 异常值（baseline 欠拟合）"""
    np.random.seed(42)
    n_samples = 200
    area = np.random.normal(loc=120, scale=30, size=n_samples)
    bedrooms = np.random.randint(1, 6, size=n_samples)
    # 真实关系：含交互项 area*bedrooms（非线性）
    price = (300 * area + 8000 * bedrooms + 60 * area * bedrooms
             + np.random.normal(0, 30000, n_samples))
    # 人为制造脏数据：前10条面积变负、后5条价格极端离群
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


if __name__ == "__main__":
    generate_v1_dataset()
