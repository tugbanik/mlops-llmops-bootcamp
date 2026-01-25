import os
from datetime import datetime, timedelta, timezone

import pandas as pd
from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select

from .database import create_db_and_tables, get_session, engine
from .models import PredictRequest, DriftRequest, ChurnPrediction, ChurnTrainingRow
from .ml_pipeline import (
    train_and_save,
    load_pipeline,
    FEATURES,
    prepare_df,
    download_dataset,
)
from .drift_detection import (
    load_reference,
    detect_numerical_drift_ks,
    detect_categorical_drift_chi2,
    quick_flags_for_single_row,
)

MODEL_PATH = os.getenv("MODEL_PATH", "app/artifacts/churn_pipeline.joblib")
REF_PATH = os.getenv("REF_PATH", "data/reference_stats.json")

DRIFT_ALPHA = float(os.getenv("DRIFT_ALPHA", "0.01"))
DEFAULT_DRIFT_DAYS = int(os.getenv("DEFAULT_DRIFT_DAYS", "7"))

app = FastAPI(title="Churn MLOps Pipeline", version="1.0.0")

_pipeline = None
_reference = None


def ensure_artifacts_and_training_table(session: Session):
    """
    - Create DB tables
    - Train model & create reference stats if missing
    - Load training data into churn_training table (one-time)
    """
    global _pipeline, _reference

    create_db_and_tables()

    # 1) ensure model + reference exist
    if not os.path.exists(MODEL_PATH) or not os.path.exists(REF_PATH):
        meta = train_and_save(MODEL_PATH, REF_PATH)
        print("TRAINED_MODEL:", meta)

    _pipeline = load_pipeline(MODEL_PATH)
    _reference = load_reference(REF_PATH)

    # 2) ensure training table is populated
    existing = session.exec(select(ChurnTrainingRow).limit(1)).first()
    if existing is None:
        df = prepare_df(download_dataset())
        rows = []
        for _, r in df.iterrows():
            rows.append(
                ChurnTrainingRow(
                    CreditScore=int(r["CreditScore"]),
                    Geography=str(r["Geography"]),
                    Gender=str(r["Gender"]),
                    Age=int(r["Age"]),
                    Tenure=int(r["Tenure"]),
                    Balance=float(r["Balance"]),
                    NumOfProducts=int(r["NumOfProducts"]),
                    HasCrCard=int(r["HasCrCard"]),
                    IsActiveMember=int(r["IsActiveMember"]),
                    EstimatedSalary=float(r["EstimatedSalary"]),
                    Exited=int(r["Exited"]),
                )
            )
        session.add_all(rows)
        session.commit()
        print(f"TRAINING_TABLE_LOADED: {len(rows)} rows")


@app.on_event("startup")
def on_startup():
    with Session(engine) as session:
        ensure_artifacts_and_training_table(session)


@app.get("/health")
def health(session: Session = Depends(get_session)):
    try:
        session.exec(select(ChurnPrediction).limit(1)).first()
        db_ok = True
    except Exception:
        db_ok = False

    return {
        "status": "ok",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "database": "ok" if db_ok else "down",
        "model_loaded": _pipeline is not None,
        "reference_loaded": _reference is not None,
    }


@app.post("/predict")
def predict(req: PredictRequest, session: Session = Depends(get_session)):
    if _pipeline is None or _reference is None:
        raise HTTPException(status_code=503, detail="Model not ready")

    row = req.model_dump()
    X = pd.DataFrame([row], columns=FEATURES)

    proba = float(_pipeline.predict_proba(X)[:, 1][0])
    pred = int(proba >= 0.5)

    # lightweight drift flags for single record
    numerical_flag, categorical_flag = quick_flags_for_single_row(row, _reference)

    rec = ChurnPrediction(
        **row,
        prediction=pred,
        probability=proba,
        numerical_drift=bool(numerical_flag),
        categorical_drift=bool(categorical_flag),
    )
    session.add(rec)
    session.commit()
    session.refresh(rec)

    return {
        "prediction": rec.prediction,
        "probability": round(rec.probability, 6),
        "prediction_id": rec.id,
        "timestamp": rec.timestamp.isoformat(),
        "drift_detection": {
            "numerical_drift": rec.numerical_drift,
            "categorical_drift": rec.categorical_drift,
            "drift_score": None,
        },
    }


@app.post("/drift/churn")
def drift_churn(payload: DriftRequest, session: Session = Depends(get_session)):
    n_days = int(payload.n_days_before)
    since = datetime.now(timezone.utc) - timedelta(days=n_days)

    # training data
    train_rows = session.exec(select(ChurnTrainingRow)).all()
    if len(train_rows) == 0:
        raise HTTPException(status_code=500, detail="Training table empty")

    train_df = pd.DataFrame([r.model_dump() for r in train_rows]).drop(columns=["id"], errors="ignore")

    # recent prediction data
    preds = session.exec(select(ChurnPrediction).where(ChurnPrediction.timestamp >= since)).all()
    if len(preds) == 0:
        return {
            "n_days_before": n_days,
            "since": since.isoformat(),
            "recent_count": 0,
            "status": "no_recent_data",
            "numerical": {},
            "categorical": {},
        }

    recent_df = pd.DataFrame([p.model_dump() for p in preds]).drop(
        columns=["id", "timestamp", "prediction", "probability", "numerical_drift", "categorical_drift"],
        errors="ignore",
    )

    num_res = detect_numerical_drift_ks(train_df, recent_df, alpha=DRIFT_ALPHA)
    cat_res = detect_categorical_drift_chi2(train_df, recent_df, alpha=DRIFT_ALPHA)

    numerical_drift_any = any(v.get("drift") for v in num_res.values())
    categorical_drift_any = any(v.get("drift") for v in cat_res.values())

    return {
        "n_days_before": n_days,
        "since": since.isoformat(),
        "recent_count": int(len(preds)),
        "drift": {
            "numerical_drift": bool(numerical_drift_any),
            "categorical_drift": bool(categorical_drift_any),
        },
        "numerical": num_res,
        "categorical": cat_res,
    }


@app.get("/drift-status")
def drift_status(session: Session = Depends(get_session)):
    since = datetime.now(timezone.utc) - timedelta(days=DEFAULT_DRIFT_DAYS)
    preds = session.exec(select(ChurnPrediction).where(ChurnPrediction.timestamp >= since)).all()

    total = len(preds)
    num_d = sum(1 for p in preds if p.numerical_drift)
    cat_d = sum(1 for p in preds if p.categorical_drift)

    return {
        "window_days": DEFAULT_DRIFT_DAYS,
        "since": since.isoformat(),
        "recent_predictions": total,
        "recent_numerical_drift_flags": num_d,
        "recent_categorical_drift_flags": cat_d,
        "recent_any_drift_flags": sum(1 for p in preds if (p.numerical_drift or p.categorical_drift)),
    }
