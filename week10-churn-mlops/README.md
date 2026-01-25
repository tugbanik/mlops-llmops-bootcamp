# Week 10 — Customer Churn Prediction  
## MLOps Pipeline with Drift Detection & Database Integration

This project was developed as part of the **MLOps & LLMOps Bootcamp**.

The goal of this assignment is to design a production-style machine learning system that includes:

- End-to-end ML pipeline
- Data drift detection
- Database-backed prediction logging
- API-based inference
- Fully containerized deployment

---

## Dataset

**Bank Customer Churn Dataset**

Source:  
https://raw.githubusercontent.com/erkansirin78/datasets/refs/heads/master/Churn_Modelling.csv

Target variable:
- **Exited**
  - 0 → Customer stays
  - 1 → Customer churns

---

## Project Objectives

- Build a reusable **scikit-learn pipeline**
- Perform **numerical and categorical drift detection**
- Log all predictions into **PostgreSQL**
- Serve predictions through **FastAPI**
- Deploy the entire system using **Docker Compose**

---

## Project Structure

week10-churn-mlops/
├── app/
│ ├── main.py # FastAPI application
│ ├── models.py # Pydantic schemas
│ ├── database.py # PostgreSQL connection
│ ├── drift_detection.py # Drift detection logic
│ └── ml_pipeline.py # Training & inference pipeline
│
├── data/
│ ├── train_model.py
│ └── reference_stats.json
│
├── screenshots/ # Project evidence
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md


---

## Machine Learning Pipeline

The model is implemented using **scikit-learn Pipelines**.

### Preprocessing
- Numerical features → `StandardScaler`
- Categorical features → `OneHotEncoder(handle_unknown="ignore")`
- Binary features → passthrough

### Model
- Logistic Regression
- `class_weight="balanced"` used for class imbalance

The full preprocessing and model steps are saved as a **single pipeline artifact**.

Artifacts:
- `churn_pipeline.joblib`
- `reference_stats.json`

---

## Drift Detection

### Numerical Drift
- Kolmogorov–Smirnov Test
- Drift threshold: **p-value < 0.01**

Monitored features:
- CreditScore
- Age
- Tenure
- Balance
- NumOfProducts
- EstimatedSalary

---

### Categorical Drift
- Chi-square test on category frequencies
- Detection of unseen categories

Monitored features:
- Geography
- Gender

---

### Online Drift Monitoring

During prediction:
- Numerical drift is triggered if values exceed training min–max ranges
- Categorical drift is triggered if unseen categories appear

Drift flags are stored together with prediction results.

---

## Database Integration

PostgreSQL is used for persistent storage.

### Tables

**churn_predictions**
- Timestamp
- Input features
- Prediction
- Prediction probability
- Numerical drift flag
- Categorical drift flag

Database operations are handled using **SQLModel**.

---

## FastAPI Endpoints

Base URL:
http://localhost:8502


### Available Endpoints

- **GET /health**  
  Checks API and database status

- **POST /predict**  
  Performs:
  - Prediction
  - Drift detection
  - Database logging

- **POST /drift/churn**  
  Compares recent prediction data with training reference

- **GET /drift-status**  
  Returns drift summary

Swagger UI:
http://localhost:8502/docs


---

## Running the Project

```bash
docker compose up --build
After startup, the API becomes available via Swagger UI.

Example Prediction Request
{
  "CreditScore": 619,
  "Geography": "France",
  "Gender": "Female",
  "Age": 42,
  "Tenure": 2,
  "Balance": 0,
  "NumOfProducts": 1,
  "HasCrCard": 1,
  "IsActiveMember": 1,
  "EstimatedSalary": 101348.88
}
Screenshots
Project execution evidence is available below:

Swagger UI
📷 screenshots/01_swagger.jpg
Prediction response
📷 screenshots/02_predict.jpg
Drift detection output
📷 screenshots/03_drift.jpg
PostgreSQL prediction records
📷 screenshots/04_db.jpg

Technologies Used
Python
scikit-learn
FastAPI
SQLModel
PostgreSQL
Docker & Docker Compose
WSL2

Summary
This project demonstrates a real-world MLOps workflow, including:
Modular ML pipeline design
Automated drift monitoring
Persistent prediction logging
API-driven inference
Fully containerized deployment

The system is reproducible, scalable, and suitable for production-style ML monitoring scenarios.
