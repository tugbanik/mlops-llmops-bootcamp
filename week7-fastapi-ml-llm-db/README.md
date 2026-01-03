# Week-7: FastAPI ML/LLM with Database Integration

This project implements database insertion for ML and LLM predictions using FastAPI.

## Implemented Endpoints

- **Advertising Prediction**
  - Saves input features and prediction result into SQLite database.
- **Iris Prediction**
  - Follows the Advertising pattern and persists prediction results.
- **Product Review Analysis (LLM)**
  - Saves review text and sentiment analysis result into the database.

## Database

- SQLite database (`app.db`) is used.
- All predictions are stored with client IP information.

## Validation

All endpoints were tested via Swagger UI.  
Database insertion was verified by checking the `db_record` field in responses.

## Screenshots

Swagger and database insertion proof screenshots are available in the `screenshots/` folder:

- Swagger endpoints overview
- Iris prediction DB record
- Advertising prediction DB record
- Product review analysis DB record
