# Week 7 — FastAPI + ML / LLM + Database

This project was developed as part of the **MLOps & LLMOps Bootcamp — Week 7 assignment**.

The goal of this week is to integrate machine learning and large language model (LLM) inference into a FastAPI backend while persisting prediction results in a database.

---

## Project Overview

This application exposes API endpoints that perform:

- Machine learning–based predictions
- LLM-powered text analysis
- Database-backed result storage

The system demonstrates how inference services can be deployed as APIs and monitored through persistent storage.

---

## Features

- FastAPI-based inference service
- Machine Learning prediction endpoint
- LLM-based text analysis endpoint
- Database persistence of prediction results
- API-level validation
- Swagger UI testing support

---

## Tech Stack

- FastAPI
- Python
- Machine Learning model
- LLM integration
- SQLite database
- SQLAlchemy / SQLModel
- Swagger / OpenAPI

---

## Project Structure

```text
week7-fastapi-ml-llm-db/
│
├── app/
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── ml_model.py
│   └── database.py
│
├── screenshots/
│   ├── 01_ml_prediction.png
│   ├── 02_llm_response.png
│   └── 03_db_records.png
│
├── requirements.txt
└── README.md
```

## API Endpoints

### ML Prediction

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /predict | Machine learning prediction |

### Query Parameters

| Parameter | Type | Description |
|----------|------|-------------|
| feature_1 | float | Input feature |
| feature_2 | float | Input feature |
| feature_3 | float | Input feature |

---

### LLM Text Analysis

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /llm | LLM-based text analysis |

### Query Parameters

| Parameter | Type | Description |
|----------|------|-------------|
| text | string | Input text for analysis|

---

## Database Fields

Prediction results are stored in a SQLite database.

| Field | Type | Description |
|------|------|-------------|
| input_data | json | Request payload |
| prediction | float | ML prediction output |
| llm_output | text | LLM response |
| created_at | datetime | Timestamp |

## Run Application

Install dependencies:

```bash
pip install -r requirements.txt
```

Start API server:
```bash
uvicorn app.main:app --reload
```

Swagger UI:
```arduino
http://127.0.0.1:8000/docs
```
---
## Screenshots

| Screenshot |  Description |
|------------|-------------|
| 01_ml_prediction.png | ML prediction endpoint  |
| 02_llm_response.png | ML prediction endpoint |
| 03_db_records.png | Database stored records |
---

## Summary

This assignment demonstrates:

* Serving ML models through APIs

* Integrating LLM inference services

* Persisting predictions in a database

* Building traceable ML inference workflows

---

## Author

**Tuğba Niksarlı**

**MLOps & LLMOps Bootcamp — Week 7**
