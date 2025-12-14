# Week 1 — MLflow Experiment Tracking & Model Registry

## Goal
Build a minimal end-to-end ML workflow and track experiments with **MLflow**:
- Train and log **3 regression models**
- Compare metrics across runs
- Register the best model in the **MLflow Model Registry**

## What I Built
This week focuses on the fundamentals of MLOps:
- reproducible training runs
- consistent metric logging
- model selection based on evaluation metrics
- model versioning through a registry

## Repository Contents
- `notebooks/` — experimentation notebook (training + MLflow logging)
- `src/` — training script(s)
- `screenshots/` — MLflow UI evidence (runs, metrics, registry)

## How to Run

### 1) Create and activate a virtual environment (optional)
```bash
python -m venv .venv
# Windows (PowerShell)
.venv\Scripts\Activate.ps1