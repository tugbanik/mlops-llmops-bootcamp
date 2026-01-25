# Week 6 — Taxi Trip API

This project was developed as part of the **MLOps & LLMOps Bootcamp — Week 6 assignment**.

The objective of this week is to build a production-style backend system that includes authentication, database integration, and protected API endpoints.

---

## Project Overview

The Taxi Trip API is a backend service that allows users to:

- Register and authenticate
- Access protected user information
- Create taxi trip records
- Retrieve stored trip data

The system is fully containerized using Docker Compose and integrates with a PostgreSQL database.

---

## Features

- User registration
- User login with JWT authentication
- Password hashing using bcrypt
- Protected endpoints with token-based access
- Taxi trip creation
- Public taxi trip listing
- PostgreSQL persistence
- Swagger UI testing support

---

## Tech Stack

- FastAPI
- PostgreSQL
- SQLAlchemy
- Docker & Docker Compose
- JWT Authentication
- bcrypt password hashing

---

## Project Structure

```text
week6-taxi-trip-api/
│
├── app/
│   ├── auth.py
│   ├── db.py
│   ├── deps.py
│   ├── main.py
│   ├── models.py
│   └── schemas.py
│
├── screenshots/
│   ├── 01_register.png
│   ├── 02_login.png
│   ├── 03_create_trip.png
│   └── 04_list_trips.png
│
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---
## API Endpoints
### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /register | Register new user |
| POST | /login | Login and receive JWT token |
| GET | /me | Get authenticated user info |

  
---
## Taxi Trips
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /trips | Create taxi trip (JWT required) |
| GET | /trips?limit=10 | Retrieve taxi trips |

---

## Running the Application
### Option 1 — Docker Compose (Recommended)
```bash
docker compose up -d
```
This will start:

* FastAPI backend

* PostgreSQL database

### Option 2 — Local Development

Install dependencies:
```bash
pip install -r requirements.txt
```
Run the API:
```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```
---

## API Documentation
Swagger UI is available at:

http://127.0.0.1:8000/docs

All endpoints can be tested interactively through Swagger.
---

## Screenshots

Screenshots below demonstrate successful execution of the API workflow:

* User registration

* User login and JWT token generation

* Creating taxi trip records

* Retrieving stored trip data
---
# Summary

In this assignment, the following backend and MLOps concepts were implemented:

* Secure authentication using JWT

* Password hashing and credential protection

* API dependency injection

* Database persistence with PostgreSQL

* Containerized backend architecture

* API testing with Swagger UI


This project represents a transition from basic APIs to production-oriented backend system design.

---
## Author
**Tuğba Niksarlı**

**MLOps & LLMOps Bootcamp — Week 6**




