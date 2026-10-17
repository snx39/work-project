# ml/data_pipeline.py
# 组员A：数据处理管线，从 v1 生成改进版 v2
# 设计说明：
#   - v2 = 数据清洗（剔除负面积、负/离群价格） + 扩充干净合成样本。
#   - 保留与 v1 相同的"非线性交互"真实关系，但数据更干净，
#     使非线性模型（如随机森林）能充分拟合 → v2 指标优于 v1 的线性 baseline。
# 用法： python ml/data_pipeline.py
import numpy as np
import pandas as pd


def build_v2(v1_path: str = "data/v1_house.csv",
             out_path: str = "data/v2_house.csv",
             n_extra: int = 300, seed: int = 7) -> pd.DataFrame:
    """清洗 v1 + 扩充合成样本，输出 v2 数据集"""
    rng = np.random.default_rng(seed)
    df = pd.read_csv(v1_path)

    # 1) 清洗：剔除负面积、负价格、以及价格 > 99% 分位的极端离群
    df = df[(df["area"] > 0) & (df["price"] > 0)]
    df = df[df["price"] < df["price"].quantile(0.99)]

    # 2) 扩充：沿用同一真实关系（含 area*bedrooms 交互项），生成干净合成样本
    extra_area = np.random.normal(loc=120, scale=25, size=n_extra)
    extra_bed = rng.integers(1, 6, size=n_extra)
    extra_price = (300 * extra_area + 8000 * extra_bed
                   + 60 * extra_area * extra_bed + rng.normal(0, 10000, n_extra))
    extra = pd.DataFrame({
        "area": extra_area.round(2),
        "bedrooms": extra_bed,
        "price": extra_price.round(2),
    })

    df_v2 = pd.concat([df, extra], ignore_index=True)
    df_v2 = df_v2.sample(frac=1, random_state=seed).reset_index(drop=True)
    df_v2.to_csv(out_path, index=False)
    print(f"Generated v2 dataset -> {out_path}, shape: {df_v2.shape}")
    return df_v2


if __name__ == "__main__":
    build_v2()
