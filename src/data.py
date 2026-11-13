"""Load the SMS Spam Collection and make a reproducible train/test split."""
from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "sms.tsv"


def load_data(path=DATA_PATH):
    df = pd.read_csv(path, sep="\t", header=None, names=["label", "message"])
    df["y"] = (df["label"] == "spam").astype(int)
    return df


def split(df, test_size=0.2, seed=42):
    return train_test_split(
        df["message"], df["y"], test_size=test_size, random_state=seed, stratify=df["y"]
    )
