from fastapi import APIRouter, Depends, Request
from sqlmodel import Session
from models import AnalyzedReview, ProductReviewRate
from database import get_db

router = APIRouter()


def analyze_review(text: str) -> str:
    # Dummy analysis (LLM bağlanmadan da çalışsın)
    return "positive"


def insert_review(review: str, result: str, client_ip: str, db: Session):
    record = ProductReviewRate(
        review=review,
        result=result,
        client_ip=client_ip,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.post("/analyze")
def analyze(payload: AnalyzedReview, fastapi_req: Request, db: Session = Depends(get_db)):
    result = analyze_review(payload.review)
    db_record = insert_review(payload.review, result, fastapi_req.client.host, db)
    return {"result": result, "db_record": db_record}
