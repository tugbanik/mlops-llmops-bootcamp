import json
import numpy as np
import pandas as pd
from scipy.stats import ks_2samp, chi2_contingency

from .ml_pipeline import NUM_COLS, CAT_COLS


def load_reference(ref_path: str) -> dict:
    with open(ref_path, "r", encoding="utf-8") as f:
        return json.load(f)


def detect_numerical_drift_ks(train_df: pd.DataFrame, recent_df: pd.DataFrame, alpha: float = 0.01) -> dict:
    """
    Numerical drift via Kolmogorov-Smirnov test.
    Drift if p_value < alpha.
    """
    results = {}
    for col in NUM_COLS:
        a = train_df[col].astype(float).dropna().values
        b = recent_df[col].astype(float).dropna().values

        if len(a) < 20 or len(b) < 20:
            results[col] = {"drift": False, "p_value": None, "note": "insufficient_sample"}
            continue

        stat, p = ks_2samp(a, b)
        results[col] = {"drift": bool(p < alpha), "p_value": float(p), "stat": float(stat)}
    return results


def detect_categorical_drift_chi2(train_df: pd.DataFrame, recent_df: pd.DataFrame, alpha: float = 0.01) -> dict:
    """
    Categorical drift via chi-square test + unseen category detection.
    Drift if p_value < alpha OR new_categories exist.
    """
    results = {}
    for col in CAT_COLS:
        train = train_df[col].astype(str).fillna("NA")
        recent = recent_df[col].astype(str).fillna("NA")

        train_cats = set(train.unique().tolist())
        recent_cats = set(recent.unique().tolist())

        new_cats = sorted(list(recent_cats - train_cats))
        all_cats = sorted(list(train_cats.union(recent_cats)))

        train_counts = train.value_counts().reindex(all_cats, fill_value=0).values
        recent_counts = recent.value_counts().reindex(all_cats, fill_value=0).values

        table = np.vstack([train_counts, recent_counts])

        if table.sum() == 0 or table.shape[1] < 2 or recent_counts.sum() < 20:
            results[col] = {"drift": False, "p_value": None, "new_categories": new_cats, "note": "insufficient_sample"}
            continue

        chi2, p, dof, _ = chi2_contingency(table)
        drift = bool(p < alpha) or (len(new_cats) > 0)

        results[col] = {
            "drift": drift,
            "p_value": float(p),
            "chi2": float(chi2),
            "dof": int(dof),
            "new_categories": new_cats,
        }
    return results


def quick_flags_for_single_row(row: dict, reference: dict) -> tuple[bool, bool]:
    """
    Lightweight per-request flags for /predict:
    - categorical_drift: unseen category vs training
    - numerical_drift: value out of training min/max (simple out-of-range)
    """
    categorical_flag = False
    for col in CAT_COLS:
        seen = set(reference["categorical"][col]["categories"])
        if str(row[col]) not in seen:
            categorical_flag = True

    numerical_flag = False
    for col in NUM_COLS:
        mn = reference["numerical"][col]["min"]
        mx = reference["numerical"][col]["max"]
        v = float(row[col])
        if v < mn or v > mx:
            numerical_flag = True

    return numerical_flag, categorical_flag
