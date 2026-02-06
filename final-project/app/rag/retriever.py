from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer


@dataclass
class RetrievedDoc:
    doc_id: str
    score: float
    excerpt: str


# docs klasörü: app/rag/docs
DOCS_DIR = Path(__file__).resolve().parent / "docs"

_vectorizer: TfidfVectorizer | None = None
_doc_ids: list[str] = []
_doc_texts: list[str] = []
_doc_matrix = None  # scipy sparse


def _read_docs() -> tuple[list[str], list[str]]:
    if not DOCS_DIR.exists():
        raise FileNotFoundError(f"Docs klasörü bulunamadı: {DOCS_DIR}")

    paths = sorted(DOCS_DIR.glob("*.md"))
    if not paths:
        raise FileNotFoundError(f"{DOCS_DIR} içinde .md doküman yok.")

    ids: list[str] = []
    texts: list[str] = []
    for p in paths:
        ids.append(p.name)
        texts.append(p.read_text(encoding="utf-8", errors="ignore"))
    return ids, texts


def _build_index() -> None:
    global _vectorizer, _doc_ids, _doc_texts, _doc_matrix

    _doc_ids, _doc_texts = _read_docs()

    _vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        min_df=1,
        lowercase=True,
    )
    _doc_matrix = _vectorizer.fit_transform(_doc_texts)


def retrieve(query: str, top_k: int = 3) -> List[RetrievedDoc]:
    """
    Basit TF-IDF retrieval:
    - docs/*.md içinden en ilgili top_k dokümanı döndürür.
    - score: cosine similarity (0..1 arası)
    """
    global _vectorizer, _doc_matrix

    if _vectorizer is None or _doc_matrix is None:
        _build_index()

    assert _vectorizer is not None
    assert _doc_matrix is not None

    q = (query or "").strip()
    if not q:
        return []

    q_vec = _vectorizer.transform([q])

    # cosine similarity: (A·B) / (||A|| ||B||)
    # TF-IDF normalize olduğu için dot product yeterli olur
    scores = (_doc_matrix @ q_vec.T).toarray().ravel()

    if scores.size == 0:
        return []

    top_k = max(1, int(top_k))
    idx = np.argsort(scores)[::-1][:top_k]

    out: list[RetrievedDoc] = []
    for i in idx:
        excerpt = _doc_texts[i][:400].replace("\n", " ").strip()
        out.append(
            RetrievedDoc(
                doc_id=_doc_ids[i],
                score=float(scores[i]),
                excerpt=excerpt,
            )
        )
    return out
