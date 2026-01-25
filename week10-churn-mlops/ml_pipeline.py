import os
import json
import joblib
import pandas as pd
import numpy as np
import requests

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression


DATA_URL = "https://raw.githubusercontent.com/erkansirin78/datasets/refs/heads/master/Churn_Modelling.csv"

NUM_COLS = ["CreditScore", "Age", "Tenure", "Balance", "NumOfProducts", "EstimatedSalary"]
CAT_COLS = ["Geography", "Gender"]
BIN_COLS = ["HasCrCard", "IsActiveMember"]

FEATURES = NUM_COLS + CAT_COLS + BIN_COLS
TARGET = "Exited"


def build_pipeline() -> Pipeline:
    """
    Full sklearn pipeline:
    - numeric: StandardScaler
    - categorical: OneHotEncoder(handle_unknown="ignore")
    - binary: passthrough
    - model: LogisticRegression
    """
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), NUM_COLS),
            ("cat", OneHotEncoder(handle_unknown="ignore"), CAT_COLS),
            ("bin", "passthrough", BIN_COLS),
        ],
        remainder="drop",
    )

    model = LogisticRegression(
        max_iter=300,
        class_weight="balanced",
    )

    pipe = Pipeline(steps=[("preprocess", preprocessor), ("model", model)])
    return pipe


def download_dataset() -> pd.DataFrame:
    r = requests.get(DATA_URL, timeout=30)
    r.raise_for_status()
    from io import StringIO
    return pd.read_csv(StringIO(r.text))


def prepare_df(df: pd.DataFrame) -> pd.DataFrame:
    # Drop ID-like columns that should not be used as features
    drop_cols = [c for c in ["RowNumber", "CustomerId", "Surname"] if c in df.columns]
    df = df.drop(columns=drop_cols)
    return df


def compute_reference_stats(df_train: pd.DataFrame) -> dict:
    """
    Save reference statistics for drift detection.
    - numerical: mean/std/min/max
    - categorical: list of categories + proportions
    """
    ref = {"numerical": {}, "categorical": {}}

    for col in NUM_COLS:
        s = df_train[col].astype(float)
        std = float(s.std(ddof=1))
        if std == 0 or np.isnan(std):
            std = 1.0
        ref["numerical"][col] = {
            "mean": float(s.mean()),
            "std": std,
            "min": float(s.min()),
            "max": float(s.max()),
        }

    for col in CAT_COLS:
        vc = df_train[col].astype(str).value_counts(dropna=False)
        total = float(vc.sum())
        ref["categorical"][col] = {
            "categories": list(vc.index.astype(str)),
            "proportions": {str(k): float(v) / total for k, v in vc.items()},
        }

    return ref


def save_reference_stats(ref: dict, ref_path: str) -> None:
    os.makedirs(os.path.dirname(ref_path), exist_ok=True)
    with open(ref_path, "w", encoding="utf-8") as f:
        json.dump(ref, f, ensure_ascii=False, indent=2)


def train_and_save(model_path: str, ref_path: str) -> dict:
    """
    Train pipeline + save model and reference stats.
    Returns basic metrics for logging.
    """
    df = prepare_df(download_dataset())

    X = df[FEATURES].copy()
    y = df[TARGET].astype(int)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    pipe = build_pipeline()
    pipe.fit(X_train, y_train)

    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    joblib.dump(pipe, model_path)

    ref_df = pd.concat([X_train, y_train.rename(TARGET)], axis=1)
    ref = compute_reference_stats(ref_df)
    save_reference_stats(ref, ref_path)

    # metric for README/log
    from sklearn.metrics import roc_auc_score
    proba = pipe.predict_proba(X_test)[:, 1]
    auc = float(roc_auc_score(y_test, proba))

    return {"roc_auc": auc, "n_train": int(len(X_train)), "n_test": int(len(X_test))}


def load_pipeline(model_path: str) -> Pipeline:
    return joblib.load(model_path)
