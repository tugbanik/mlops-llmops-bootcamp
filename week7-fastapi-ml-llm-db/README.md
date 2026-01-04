# Week 7 – FastAPI + ML / LLM with Database Persistence

This project is developed as part of the **MLOps & LLMOps Bootcamp – Week 7** assignment.

The main goal of this week is to build a FastAPI application that integrates:
- Machine Learning / LLM-based endpoints
- Database persistence
- End-to-end request → prediction → storage flow

---

## Project Overview

The API exposes multiple endpoints that:
- Accept structured input data
- Generate predictions using ML / LLM logic
- Persist prediction results into a SQLite database
- Allow verification via Swagger UI

All database operations are handled using SQLAlchemy ORM.

---

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- SQLite (local, runtime-generated)
- Pydantic
- Swagger / OpenAPI

---

## Project Structure

```text
week7-fastapi-ml-llm-db/
├── main.py
├── database.py
├── models.py
├── requirements.txt
├── screenshots/
│   ├── 01_swagger_endpoints.png
│   ├── 02_iris_db_record.png
│   ├── 03_advertising_db_record.png
│   └── 04_product_review_db_record.png
└── README.md
