# Final Project – Special Education Support Assistant (Architecture Overview)

This folder documents the architectural design of my final project developed during the MLOps & LLMOps Bootcamp.

Implementation details and code are maintained in a private repository.

## Objective
Design a safety-aware, modular support assistant system that provides structured, non-clinical recommendations for special education contexts.

## Architecture

```mermaid
flowchart LR
    U[User] --> API[FastAPI Service]
    API --> CLS[Topic Classification]
    CLS --> RET[Guideline Retrieval Engine]
    RET --> GEN[Structured Response Generator]
    GEN --> DB[(Database)]
    DB --> REP[Reporting Layer]

    style API fill:#E3F2FD
    style CLS fill:#FFF3E0
    style RET fill:#E8F5E9
    style GEN fill:#F3E5F5
    style DB fill:#FCE4EC
    style REP fill:#E0F7FA