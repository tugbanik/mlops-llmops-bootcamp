# Week 6 – Taxi Trip API

This project is developed as part of the MLOps & LLMOps Bootcamp Week-6 assignment.

## Features
- User Registration (`POST /register`)
- User Login with JWT (`POST /login`)
- Protected endpoint (`GET /me`)
- Create taxi trip **one at a time** (`POST /trips`, JWT required)
- Retrieve trips (`GET /trips?limit=10`, public)

## Tech Stack
- FastAPI
- PostgreSQL (Docker Compose)
- SQLAlchemy
- JWT Authentication
- bcrypt password hashing

## Run Locally

```bash
docker compose up -d
pip install -r requirements.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
