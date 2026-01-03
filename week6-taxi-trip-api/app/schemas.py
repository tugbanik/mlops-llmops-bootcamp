from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


class RegisterRequest(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=6, max_length=72)
    email: EmailStr | None = None


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class TripCreate(BaseModel):
    VendorID: int
    tpep_pickup_datetime: datetime
    tpep_dropoff_datetime: datetime

    passenger_count: float
    trip_distance: float
    RatecodeID: float

    store_and_fwd_flag: str = Field(..., min_length=1, max_length=1)

    PULocationID: int
    DOLocationID: int

    payment_type: int

    fare_amount: float
    extra: float
    mta_tax: float
    tip_amount: float
    tolls_amount: float
    improvement_surcharge: float
    total_amount: float
    congestion_surcharge: float
    Airport_fee: float

    row_id: str | None = None


class TripOut(BaseModel):
    row_id: str
    VendorID: int
    tpep_pickup_datetime: datetime
    tpep_dropoff_datetime: datetime
    passenger_count: float
    trip_distance: float
    total_amount: float

    class Config:
        from_attributes = True
