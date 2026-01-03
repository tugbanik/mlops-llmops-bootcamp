from sqlmodel import SQLModel, Field
from typing import Optional


# -------------------------
# Advertising (REFERENCE)
# -------------------------
class Advertising(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    tv: float
    radio: float
    newspaper: float
    prediction: float
    client_ip: Optional[str] = None


# -------------------------
# Iris
# -------------------------
class Iris(SQLModel):
    SepalLengthCm: float
    SepalWidthCm: float
    PetalLengthCm: float
    PetalWidthCm: float


class IrisPrediction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    SepalLengthCm: float
    SepalWidthCm: float
    PetalLengthCm: float
    PetalWidthCm: float
    prediction: str
    client_ip: Optional[str] = None


# -------------------------
# Product Review (LLM)
# -------------------------
class AnalyzedReview(SQLModel):
    review: str


class ProductReviewRate(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    review: str
    result: str
    client_ip: Optional[str] = None