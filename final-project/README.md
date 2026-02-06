# Special Education Support Assistant (Bootcamp MVP)

This project is a **Bootcamp MVP** developed within the MLOps & LLMOps Bootcamp.

The system provides **structured support recommendations** for parents and educators of children with special needs, based on:
- Machine Learning classification
- Document-based retrieval (RAG-style, no external LLM)
- Rule & template-driven response generation
- Persistent storage and feedback collection

---

## 🎯 Project Goal

- Accept a natural language question about a child with special needs
- Predict the topic using a trained ML classifier
- Retrieve relevant guideline documents
- Generate structured, safe, non-clinical recommendations
- Store interactions and feedback in a database

---

## 🧠 System Architecture

User Question
↓
ML Classifier (predict_label)
↓
Document Retriever (RAG - local markdown files)
↓
Rule & Template-based Generator
↓
API Response + Database Storage


---

## 🧩 Key Components

### FastAPI
- `/health` – service health check
- `/ask_support` – main inference endpoint
- `/feedback` – user feedback collection

### Machine Learning
- Classical text classification model
- Trained on labeled support / education / health / administrative examples
- Loaded at application startup

### RAG (No External LLM)
- Local markdown documents
- Simple similarity-based retrieval
- Safe, offline, reproducible MVP design

### Database
- SQLite via SQLModel
- Stores:
  - user question
  - predicted label
  - generated answer
  - timestamps
  - feedback

---

## 🐳 Running the Project

```bash
docker compose build --no-cache
docker compose up -d

Swagger UI:
http://localhost:8000/docs

Health check:
http://localhost:8000/health

---
⚠️ Disclaimer

This system does not provide medical or clinical advice.
For urgent or critical situations, professional support should be consulted.
---
📌 Bootcamp Context

This project demonstrates:

API design

ML inference integration

RAG-style retrieval

Database persistence

Dockerized deployment

External LLM APIs were intentionally not used to keep the MVP offline and reproducible.
---

---

## 4️⃣ `.gitignore` kontrolü (çok önemli)
Repo kökünde `.gitignore` aç → şu satır **var mı** bak:
---
*.db

---

## 5️⃣ GitHub’a gönderme (tek seferde)
```bash
git add final-project
git commit -m "Add Special Education Support Assistant MVP"
git push origin main
