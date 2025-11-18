# Job Lead Generator

### Automated Job Application Assistant with Retrieval, Ranking, and Agentic Workflows

This project was created to solve a personal, practical problem: applying for jobs involves repetitive tasks, manual comparisons, and repeated rewriting of documents (resume, cover letter) to improve the chances of being selected.

The goal of this system is to automate large parts of that workflow, saving time, reducing repetitive work load, and providing objective evaluations of how well a candidate fits a job posting. The platform extracts job postings, analyzes requirements, evaluates skill fit, and generates application materials on demand.

> This project aims to automate the <b>"mechanical”</b> parts (retrieval, comparison, document generation) while leaving humans to focus on decision-making and actual career strategy.

## Overview

The system consists of:
- A browser extension that captures job descriptions directly from LinkedIn/Indeed.

- A backend service (FastAPI) for data processing, retrieval, and generation.

- A vector-based retrieval layer for semantic comparison of job posts and user profiles.

- Agentic workflows (LangChain/LangGraph) for tailoring resumes, generating cover letters, and performing skill-gap analysis.

## Core Features

1. <b>Job Capture (Browser Extension):</b>

    Extract job posting content from DOM. Optional manual text selection. Store raw job descriptions in MongoDB for later analysis.

2. <b>Job Matching & Ranking</b>

    Uses vector similarity search (pgvector/Chroma) to compare saved job postings with the user’s profile. LangChain pipelines compute:
    - Skill/experience overlap
    - Semantic similarity scores
    - Ranked list of best-fit roles

3. <b>Resume Tailoring</b>

    A LangChain agent retrieves the most relevant job requirements and rewrites resume sections accordingly. Highlights aligned skills and adjusts bullet points to match role expectations.

4. <b>Cover Letter Generation</b>

    RAG workflow retrieves job details + user background and generates a structured cover letter via LangChain. Retrieval ensures contextually accurate, job-specific output.

5. <b>Skill Gap Analysis</b>

    Extracts required skills from job embeddings and compares them with the user’s skill vectors. The LangChain pipeline surfaces missing skills and provides improvement suggestions.

### Technologies Used
- FastAPI (API layer, typed models (pydantic), clean structure)
- MongoDB (raw job storage)
- pgvector / Qdrant (vector search)
- LangChain / LangGraph (tool-based agent workflows)
- Gemini (LLM generation, Embedding)
- Docker (local orchestration)
- Langsmith (experiment tracking)