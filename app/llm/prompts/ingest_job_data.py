''' LLM Prompts for Ingesting Job Data '''

from functools import lru_cache
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate

prompt_template = """
    You are an expert job-description normalizer designed for candidate–job retrieval systems.

    You will receive job data which may be raw text or HTML.  
    Your task is to clean, normalize, and structure it following format:{format_instructions}.

    ***STEP 1 — CLEANING***
    - Remove all HTML tags and formatting noise.
    - Remove navigation text, template text, tracking text, numbers, symbols, or unrelated boilerplate.
    - Normalize into high-quality plain text.

    ***STEP 2 — JOB METADATA EXTRACTION***
    Extract:
    - Job title
    - Company name
    - Location (if present; otherwise null)
    - Skills (only technical or job-relevant ones)

    If a field cannot be determined, return `null`.

    ***STEP 3 — CORE DESCRIPTION NORMALIZATION***
    Convert the cleaned job description into **5–7 concise, high-signal key requirements**, each:
    - 15–20 words maximum  
    - directly related to what the job expects  
    - merged/normalized for duplicates  
    - technical, skill-focused, and retrieval-friendly  
    - no fluff, stay objective and precise (as ATS systems prefers)

    These key points will be used for semantic vector search, so optimize for clarity, precision, and recall.

    Job Content:
    {job_data}
    """

@lru_cache()
def get_ingest_job_data_prompt() -> ChatPromptTemplate:
    return ChatPromptTemplate.from_messages([
        HumanMessagePromptTemplate.from_template(prompt_template)
    ])
