# src/data_loader.py

import pandas as pd


def load_products(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    text_cols = ["name", "brand", "category_label", "occasion", "tags", "description"]
    for col in text_cols:
        df[col] = df[col].fillna("").astype(str)
    df["search_text"] = (
        df["name"] + " "
        + df["brand"] + " "
        + df["category_label"] + " "
        + df["occasion"] + " "
        + df["tags"] + " "
        + df["description"]
    ).str.strip()
    return df


def load_outfits(path: str) -> pd.DataFrame:
    df = pd.read_csv(path).fillna("")
    return df