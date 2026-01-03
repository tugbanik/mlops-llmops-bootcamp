from fastapi import APIRouter, Depends, Request
from sqlmodel import Session
from models import Advertising
from database import get_db

router = APIRouter()


def insert_advertising(tv: float, radio: float, newspaper: float, prediction: float, client_ip: str, db: Session):
    record = Advertising(
        tv=tv,
        radio=radio,
        newspaper=newspaper,
        prediction=prediction,
        client_ip=client_ip,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.post("/predict")
def predict_advertising(tv: float, radio: float, newspaper: float, fastapi_req: Request, db: Session = Depends(get_db)):
    # Basit/dummy prediction (pattern göstermek için)
    prediction = float(0.0)

    db_record = insert_advertising(tv, radio, newspaper, prediction, fastapi_req.client.host, db)
    return {"prediction": prediction, "db_record": db_record}