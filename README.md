# Job Lead Generator

Job Lead Generator is a backend service that automates retrieval, semantic ranking, and GenAI-driven generation of application materials (resumes and cover letters). It extracts and normalizes job postings, assesses candidate-job fit, retrieves high-quality contextual information via vector search and RAG fusion, and executes schema-validated LLM pipelines to produce role-specific documents—reducing repetitive work and speeding application preparation.

This repository contains the backend implementation: a FastAPI API with JWT authentication, Celery-based asynchronous orchestration for LLM tasks, LangChain workflows with schema validation, and Qdrant-powered retrieval. Frontend and UX components are planned for future development.

## What’s implemented (backend-focused)

- FastAPI backend with typed Pydantic models and clear, service-oriented structure.
- JWT authentication for API endpoints.
- Celery-driven asynchronous orchestration for LLM tasks (resume & cover letter generation).
- LangChain-based, multi-step generation workflows with schema validation to ensure reliable pipelines.
- Multi-Query and RAG Fusion retrieval using Qdrant for high-quality context retrieval.
- Vector store and retrieval layer abstractions (pluggable vector DB).
- MongoDB for raw job storage and PostgreSQL schema scaffolding where applicable.
- Object-store adapters (S3-compatible) and file helpers for artifact management.
- Structured logging, config separation, and Docker-ready deployment artifacts.

## High-level architecture

- API layer (FastAPI): auth, document generation endpoints, docs routers.
- Async task layer (Celery): long-running LLM jobs, background generation and artifact persistence.
- Retrieval layer (Qdrant / vector store): multi-query retrieval + RAG fusion to assemble context.
- LLM layer (LangChain + embeddings): schema-validated prompts and generation flows.
- Storage: MongoDB for raw job posts, object store for documents, optional Postgres for relational data.

## Core features and workflows

- Job capture (planned): browser extension to capture job postings into MongoDB.
- Job matching & ranking (backend ready): vector/semantic matching and scoring pipelines to surface best-fit roles.
- Resume tailoring (backend ready): LangChain agents tailor resume sections to job requirements.
- Cover letter generation (backend ready): RAG-powered generation that combines retrieved job context + user profile.
- Skill-gap analysis (planned/enhanced): schemas and pipelines are in place; richer analytics and UI are pending.

## Directory overview (backend)
- app/main.py — FastAPI entrypoint
- app/api — API routers (auth, docs/coverletter, docs/resume)
- app/core — config, logging, Celery config, exceptions
- app/db — vector store, object store, Mongo adapters
- app/llm — embeddings, prompts, LLM models and prompts
- app/services — resume & cover-letter generation services
- app/tasks — Celery tasks that wrap LLM workflows

## Run & access Swagger API docs (step-by-step)

1. Clone the repo and enter the project directory:
```bash
git clone https://github.com/singh-nilesh/job-lead-gen.git
cd job-lead-gen
```

2. Copy the example environment and update secrets:
```bash
cp .env.example .env
# edit .env and set JWT, DB, Qdrant, S3, LLM keys, etc.
```

3. Build and start services with Docker Compose:
```bash
docker compose up --build -d
```

4. Open the FastAPI Swagger UI:
```
http://localhost:8000/docs
```

To stop services:
```bash
docker compose down
```

Note: If the service binds to a different port, replace 8000 in the URL. See app/core/celery_config.py and app/core/config.py for runtime settings.

## Future work (non-exhaustive)

- Browser extension for job capture (LinkedIn/Indeed DOM extraction).
- Web UI for application management and review.
- End-to-end ingestion pipelines and scheduled scrapers.
- Expanded LLM/provider integrations and more robust experiment tracking.
- End-to-end tests and CI/CD for deployments and model/version governance.