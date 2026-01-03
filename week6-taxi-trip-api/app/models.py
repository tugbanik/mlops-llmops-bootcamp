from sqlalchemy import Column, Integer, String, Float, DateTime
from .db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    email = Column(String(255), nullable=True)


class Trip(Base):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, index=True)

    VendorID = Column(Integer, nullable=False)
    tpep_pickup_datetime = Column(DateTime, nullable=False)
    tpep_dropoff_datetime = Column(DateTime, nullable=False)

    passenger_count = Column(Float, nullable=False)
    trip_distance = Column(Float, nullable=False)
    RatecodeID = Column(Float, nullable=False)

    store_and_fwd_flag = Column(String(1), nullable=False)

    PULocationID = Column(Integer, nullable=False)
    DOLocationID = Column(Integer, nullable=False)

    payment_type = Column(Integer, nullable=False)

    fare_amount = Column(Float, nullable=False)
    extra = Column(Float, nullable=False)
    mta_tax = Column(Float, nullable=False)
    tip_amount = Column(Float, nullable=False)
    tolls_amount = Column(Float, nullable=False)
    improvement_surcharge = Column(Float, nullable=False)
    total_amount = Column(Float, nullable=False)
    congestion_surcharge = Column(Float, nullable=False)
    Airport_fee = Column(Float, nullable=False)

    row_id = Column(String(64), unique=True, index=True, nullable=False)