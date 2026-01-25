import os
import sys

# allow running from /code/data inside container OR from project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.ml_pipeline import train_and_save

MODEL_PATH = os.getenv("MODEL_PATH", "app/artifacts/churn_pipeline.joblib")
REF_PATH = os.getenv("REF_PATH", "data/reference_stats.json")

if __name__ == "__main__":
    meta = train_and_save(MODEL_PATH, REF_PATH)
    print("Training complete:", meta)
