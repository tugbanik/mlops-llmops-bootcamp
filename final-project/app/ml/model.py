from __future__ import annotations

from pathlib import Path
import os

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

# Bu dosyanın bulunduğu klasör: .../app/ml
HERE = Path(__file__).resolve().parent

# Modeli app/ml altına kaydedelim (container içinde de stabil)
MODEL_PATH = HERE / "model.joblib"

# train.csv'yi önce env'den (opsiyonel), yoksa app/ml/train.csv'den oku
TRAIN_PATH = Path(os.getenv("TRAIN_PATH", str(HERE / "train.csv")))

_model: Pipeline | None = None


def load_model() -> None:
    """
    Container içinde startup'ta çağrılır.
    Model varsa yükler; yoksa train.csv'den hızlıca eğitir ve kaydeder.
    """
    global _model

    if MODEL_PATH.exists():
        _model = joblib.load(MODEL_PATH)
        return

    if not TRAIN_PATH.exists():
        raise FileNotFoundError(
            f"train.csv bulunamadı: {TRAIN_PATH}. "
            "Dosyayı app/ml/train.csv olarak koy "
            "ya da TRAIN_PATH env ile yolu ver."
        )

    df = pd.read_csv(TRAIN_PATH, encoding="utf-8")
    if "text" not in df.columns or "label" not in df.columns:
        raise ValueError("train.csv kolonları text,label olmalı.")

    X = df["text"].astype(str).fillna("")
    y = df["label"].astype(str).fillna("")

    pipeline = Pipeline(
        steps=[
            ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=1)),
            ("clf", LogisticRegression(max_iter=1000)),
        ]
    )
    pipeline.fit(X, y)

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, MODEL_PATH)
    _model = pipeline


def predict_label(text: str) -> str:
    global _model
    if _model is None:
        load_model()

    #assert _model is not None
    return str(_model.predict([str(text)])[0])
