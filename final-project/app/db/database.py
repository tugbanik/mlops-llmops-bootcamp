from __future__ import annotations

import os
from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field, create_engine


DB_PATH = os.getenv("DB_PATH", "/app/data/app.db")
DB_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(DB_URL, echo=False)


class Interaction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    question: str
    answer: str

    prompt_version: str = "v1"
    docs_version: str = "v1"
    top_k: int = 3

    predicted_label: Optional[str] = None

    # JSON string olarak saklayacağız (doc_id listesi / score listesi)
    retrieved_docs: Optional[str] = None
    retrieved_scores: Optional[str] = None


class Feedback(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    interaction_id: int = Field(index=True)
    rating: int = Field(ge=1, le=5)
    comment: Optional[str] = None


def init_db() -> None:
    SQLModel.metadata.create_all(engine)
