import hashlib
import json

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .db import engine
from . import models
from .deps import get_db
from .schemas import RegisterRequest, TokenResponse, TripCreate, TripOut
from .auth import hash_password, verify_password, create_access_token, get_current_user

# Tabloları DB'de oluşturdum
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Taxi Trip API")


@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/register")
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.username == payload.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already registered")

    user = models.User(
        username=payload.username,
        password_hash=hash_password(payload.password),
        email=payload.email,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "user created", "username": user.username}


@app.post("/login", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    token = create_access_token(data={"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}


@app.get("/me")
def me(username: str = Depends(get_current_user)):
    return {"username": username}
@app.post("/trips")
def create_trip(
    payload: TripCreate,
    db: Session = Depends(get_db),
    username: str = Depends(get_current_user),  # <- AUTH burada
):
    # row_id yoksa deterministic üret (aynı payload -> aynı row_id)
    if payload.row_id:
        row_id = payload.row_id
    else:
        data_for_hash = payload.model_dump(exclude={"row_id"})
        raw = json.dumps(data_for_hash, default=str, sort_keys=True).encode("utf-8")
        row_id = hashlib.md5(raw).hexdigest()

    # aynı row_id tekrar eklenmesin
    existing = db.query(models.Trip).filter(models.Trip.row_id == row_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Trip with this row_id already exists")

    trip = models.Trip(**payload.model_dump(exclude={"row_id"}), row_id=row_id)

    db.add(trip)
    db.commit()
    return {"message": "trip created", "row_id": row_id}
@app.get("/trips", response_model=list[TripOut])
def list_trips(limit: int = 10, db: Session = Depends(get_db)):
    limit = min(max(limit, 1), 10)  # 1..10
    trips = (
        db.query(models.Trip)
        .order_by(models.Trip.tpep_pickup_datetime.desc())
        .limit(limit)
        .all()
    )
    return trips
