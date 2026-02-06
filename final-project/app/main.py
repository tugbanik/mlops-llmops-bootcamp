from __future__ import annotations

import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlmodel import Session

from app.db.database import engine, init_db, Interaction, Feedback
from app.ml.model import load_model, predict_label

from app.rag.retriever import retrieve
from app.rag.generator import generate_answer


app = FastAPI(
    title="Special Education Support Assistant (Bootcamp MVP)",
    version="0.1.0",
    description=(
        "RAG-based support assistant for parents and educators of children "
        "with special needs. This is a bootcamp MVP (no external LLM)."
    ),
)

# Swagger'da bazen görülen "Failed to fetch" / eklenti-origin sorunları için
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # MVP için serbest; prod'da kısıtlanır
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    init_db()
    load_model()  # modeli startup'ta yükle/eğit (container içinde stabil)


class AskRequest(BaseModel):
    question: str


class AskResponse(BaseModel):
    interaction_id: int
    answer: str
    disclaimer: str
    topic_label: str


class FeedbackRequest(BaseModel):
    interaction_id: int
    rating: int
    comment: str | None = None


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/ask_support", response_model=AskResponse)
def ask_support(payload: AskRequest):
    # 1) Uyarı metni
    disclaimer_text = (
        "Bu sistem tıbbi/klinik tanı veya acil müdahale önerisi vermez. "
        "Acil risk veya güvenlik endişesi varsa lütfen bir uzmana/112'ye başvurun."
    )

    # 2) ML sınıflandırma (label tahmini)
    label = predict_label(payload.question)

    # 3) RAG retrieve (doküman seç)
    docs = retrieve(payload.question, top_k=3)

    # 4) LLM yok: template/rules + docs parçalarıyla cevap üret
    answer_text = generate_answer(
        question=payload.question,
        label=label,
        docs=docs,
    )

    # 5) DB’ye yaz (retrieved doc id/score'ları da saklayalım)
    retrieved_doc_ids = [getattr(d, "doc_id", None) for d in docs]
    retrieved_scores = [getattr(d, "score", None) for d in docs]

    with Session(engine) as session:
        interaction = Interaction(
            question=payload.question,
            answer=answer_text,
            predicted_label=label,
            prompt_version="v1",
            docs_version="v1",
            top_k=3,
            retrieved_docs=json.dumps(retrieved_doc_ids, ensure_ascii=False),
            retrieved_scores=json.dumps(retrieved_scores, ensure_ascii=False),
        )
        session.add(interaction)
        session.commit()
        session.refresh(interaction)

    # 6) Response
    return AskResponse(
        interaction_id=interaction.id,
        answer=answer_text,
        disclaimer=disclaimer_text,
        topic_label=label,
    )


@app.post("/feedback")
def submit_feedback(payload: FeedbackRequest):
    with Session(engine) as session:
        fb = Feedback(
            interaction_id=payload.interaction_id,
            rating=payload.rating,
            comment=payload.comment,
        )
        session.add(fb)
        session.commit()

    return {"status": "saved"}
