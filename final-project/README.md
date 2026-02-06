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
ML Classifier (`predict_label`)  
↓  
Document Retriever (RAG – local markdown files)  
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

## ✅ DB Validation Strategy (How We Verify Persistence)

This MVP uses SQLite (SQLModel) for persistence.

To keep the Docker image minimal, the `sqlite3` CLI is **not installed** inside the container.

Instead, database writes are validated at the **API boundary**:

- `/ask_support` returns an `interaction_id` after persisting the interaction  
- `/feedback` returns `{ "status": "saved" }` after persisting the feedback  
- `docker compose logs api` shows:
  - `POST /ask_support 200`
  - `POST /feedback 200`

This approach is aligned with production practices where **direct DB shell access is typically avoided**.

---

## 📊 Reporting & Monitoring

The project includes a lightweight reporting layer to monitor system usage and output quality.

- `scripts/report_daily.py`  
  Reads interaction and feedback data from the SQLite database and generates a daily summary report.

- `reports/summary.md`  
  Automatically generated markdown report including:
  - total number of interactions
  - total feedback count
  - average user rating
  - positive feedback rate (rating ≥ 4)
  - Wilson confidence interval (small-sample aware)
  - most frequent user questions

This component demonstrates basic **post-inference statistical monitoring**, rather than offline model accuracy evaluation.



---
## 🐳 Running the Project

```bash
docker compose build --no-cache
docker compose up -d
```

Swagger UI:
http://localhost:8000/docs

Health check:
http://localhost:8000/health

## ⚠️ Disclaimer

This system does not provide medical or clinical advice.
For urgent or critical situations, professional support should be consulted.

## 📌 Bootcamp Context
This project demonstrates:

- API design

- ML inference integration

- RAG-style retrieval

- Database persistence

- Dockerized deployment

- External LLM APIs were intentionally not used to keep the MVP offline and reproducible.

## 🧾 .gitignore Note

Local database files are intentionally ignored:
```
*.db 
```

## 🚀 GitHub Push
```bash
git add final-project
git commit -m "Update README: add DB validation strategy"
git push origin main
```