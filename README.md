# MLOps & LLMOps Bootcamp

This repository contains my weekly assignments and projects developed during the **MLOps & LLMOps Bootcamp**.  
Each folder corresponds to a specific week and focuses on a particular MLOps / backend / ML system concept.

---

## Repository Structure

```text
mlops-llmops-bootcamp/
│
├── week1-linux-basics/
│   └── Linux fundamentals and command-line exercises
│
├── week5-fastapi-sum-api/
│   └── Simple FastAPI application with basic endpoint testing
│
├── week6-taxi-trip-api/
│   ├── app/
│   │   ├── auth.py
│   │   ├── db.py
│   │   ├── deps.py
│   │   ├── main.py
│   │   ├── models.py
│   │   └── schemas.py
│   ├── screenshots/
│   │   ├── 01_register.png
│   │   ├── 02_login.png
│   │   ├── 03_create_trip.png
│   │   └── 04_list_trips.png
│   ├── docker-compose.yml
│   ├── requirements.txt
│   └── README.md
│
├── week7-fastapi-ml-llm-db/
│   └── FastAPI + ML/LLM endpoints with database persistence
│
├── week10-churn-mlops/
│   ├── app/
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── database.py
│   │   ├── drift_detection.py
│   │   └── ml_pipeline.py
│   ├── data/
│   │   ├── train_model.py
│   │   └── reference_stats.json
│   ├── screenshots/
│   │   ├── 01_swagger.jpg
│   │   ├── 02_predict.jpg
│   │   ├── 03_drift.jpg
│   │   └── 04_db.jpg
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── requirements.txt
│   └── README.md
│
└── README.md

## Week Highlights

---

### Week 1 — Linux Basics

Linux terminal and filesystem fundamentals.

- Directory and file operations  
- Basic shell commands  
- Command-line workflow familiarity  

---

### Week 5 — FastAPI Sum API

Introduction to backend development with FastAPI.

- Simple REST API structure  
- Request–response handling  
- Endpoint testing with Swagger UI  

---

### Week 6 — Taxi Trip API

Backend system with authentication and database integration.

- JWT-based authentication  
- PostgreSQL with Docker Compose  
- User registration and login  
- Protected endpoints  
- Taxi trip creation and listing  
- Swagger UI validation  
- Screenshot-based proof of execution  

---

### Week 7 — FastAPI + ML / LLM + Database

Machine learning and LLM inference services with persistence.

- ML and LLM-based prediction endpoints  
- Database-backed result storage  
- API-level validation  
- Swagger UI testing  
- Execution screenshots  

---

### Week 10 — Customer Churn Prediction (MLOps Pipeline)

End-to-end MLOps pipeline implementation.

- Scikit-learn pipeline for preprocessing and modeling  
- Numerical and categorical drift detection  
- PostgreSQL-based prediction logging  
- FastAPI inference service  
- Dockerized deployment with Docker Compose  
- Operational validation via screenshots  

---



Tech Stack (Overall)

Python
FastAPI
SQLAlchemy / SQLModel
PostgreSQL & SQLite
Docker & Docker Compose
JWT Authentication
Machine Learning Pipelines
Data Drift Detection
Swagger / OpenAPI

Notes
Each week is isolated in its own folder.
Screenshots are included where required as proof of execution.
Detailed explanations are provided inside each week's README.md.

Author
Tuğba Niksarlı
MLOps & LLMOps Bootcamp Participant
