from fastapi import APIRouter, Depends, Request
from sqlmodel import Session
from models import Iris, IrisPrediction
from database import get_db

router = APIRouter()


def make_iris_prediction(input_data: Iris) -> str:
    # Dummy prediction (model dosyası yoksa bile API çalışsın)
    return "setosa"


def insert_iris(input_data: Iris, prediction: str, client_ip: str, db: Session):
    record = IrisPrediction(
        SepalLengthCm=input_data.SepalLengthCm,
        SepalWidthCm=input_data.SepalWidthCm,
        PetalLengthCm=input_data.PetalLengthCm,
        PetalWidthCm=input_data.PetalWidthCm,
        prediction=prediction,
        client_ip=client_ip,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.post("/predict")
def predict_iris(payload: Iris, fastapi_req: Request, db: Session = Depends(get_db)):
    prediction = make_iris_prediction(payload)
    db_record = insert_iris(payload, prediction, fastapi_req.client.host, db)
    return {"prediction": prediction, "db_record": db_record}
