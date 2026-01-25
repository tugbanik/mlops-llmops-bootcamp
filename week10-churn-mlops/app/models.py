from datetime import datetime, timezone
from typing import Optional
from sqlmodel import SQLModel, Field

# -------------------------
# TRAINING DATA TABLE
# -------------------------

class ChurnTrainingRow(SQLModel, table=True):
    __tablename__ = "churn_training"

    id: Optional[int] = Field(default=None, primary_key=True)

    CreditScore: int
    Geography: str
    Gender: str
    Age: int
    Tenure: int
    Balance: float
    NumOfProducts: int
    HasCrCard: int
    IsActiveMember: int
    EstimatedSalary: float

    Exited: int


# -------------------------
# PREDICTION TABLE
# -------------------------

class ChurnPrediction(SQLModel, table=True):
    __tablename__ = "churn_predictions"

    id: Optional[int] = Field(default=None, primary_key=True)
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    CreditScore: int
    Geography: str
    Gender: str
    Age: int
    Tenure: int
    Balance: float
    NumOfProducts: int
    HasCrCard: int
    IsActiveMember: int
    EstimatedSalary: float

    prediction: int
    probability: float

    numerical_drift: bool = False
    categorical_drift: bool = False


# -------------------------
# API REQUEST MODELS
# -------------------------

class PredictRequest(SQLModel):
    CreditScore: int
    Geography: str
    Gender: str
    Age: int
    Tenure: int
    Balance: float
    NumOfProducts: int
    HasCrCard: int
    IsActiveMember: int
    EstimatedSalary: float


class DriftRequest(SQLModel):
    n_days_before: int = 7
