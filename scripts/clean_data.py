"""
Clean the raw Ames Housing dataset and save a cleaned CSV for modeling and demos.

Usage (PowerShell):
  .venv\Scripts\python.exe scripts/clean_data.py

Input: data/AmesHousing.csv
Output: docs/datasets/ames_clean.csv
"""
from __future__ import annotations
import pandas as pd
from pathlib import Path

RAW = Path(__file__).resolve().parents[1] / "data" / "AmesHousing.csv"
OUT = Path(__file__).resolve().parents[1] / "docs" / "datasets" / "ames_clean.csv"


def clean(df: pd.DataFrame) -> pd.DataFrame:
    # Drop id-like columns if present
    for col in ("PID", "Order", "Id"):
        if col in df.columns:
            df = df.drop(columns=[col])

    # Fill numeric with median, categorical with mode
    num_cols = df.select_dtypes(include=["int64", "float64"]).columns
    cat_cols = df.select_dtypes(include=["object"]).columns

    for c in num_cols:
        if df[c].isna().any():
            df[c] = df[c].fillna(df[c].median())
    for c in cat_cols:
        if df[c].isna().any():
            df[c] = df[c].fillna(df[c].mode().iloc[0])

    # Basic outlier trim on SalePrice if present
    if "SalePrice" in df.columns:
        s = df["SalePrice"]
        m, sd = s.mean(), s.std()
        df = df[(s >= m - 2.5 * sd) & (s <= m + 2.5 * sd)]

    return df


def main() -> None:
    df = pd.read_csv(RAW)
    cleaned = clean(df)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    cleaned.to_csv(OUT, index=False)
    print(f"Saved cleaned dataset to {OUT}")


if __name__ == "__main__":
    main()
