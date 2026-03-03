# Final Project – Special Education Support Assistant (Architecture Overview)

This folder documents the architectural design of my final project developed during the MLOps & LLMOps Bootcamp.

Implementation details and code are maintained in a private repository.

## Objective
Design a safety-aware, modular support assistant system that provides structured, non-clinical recommendations for special education contexts.

## Architecture

```mermaid
flowchart TD
    A[User] --> B[API Layer]
    B --> C[Classification]
    C --> D[Guideline Retrieval]
    D --> E[Structured Response]
    E --> F[Persistence Layer]
    F --> G[Lightweight Reporting]