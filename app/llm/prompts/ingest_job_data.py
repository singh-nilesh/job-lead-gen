''' LLM Prompts for Ingesting Job Data '''

from functools import lru_cache
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate


@lru_cache()
def get_ingest_job_data_prompt() -> ChatPromptTemplate:
    return ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.format(
            """
    You are an expert job-description normalizer designed for candidate–job retrieval systems.

    You will receive job data which may be raw text or HTML.  
    Your task is to clean, normalize, and structure it following.

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

    output format:{format_instructions}.
    """),
        HumanMessagePromptTemplate.from_template(
            " generate the structured job data for following job data:{job_data}"
        )
    ])


@lru_cache()
def get_cover_letter_multi_query_prompt() -> ChatPromptTemplate:
    return ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(
            """
    You are a retrieval-query generator for cover-letter construction.
    You do NOT write the cover letter. Your job is to generate short
    semantic queries that retrieve the most relevant experience snippets
    from a vector store.
    
    You will receive *job data* which may be raw text or HTML. Your task is to extract text
    and clean it up, then generate retrieval queries based on the job description and any personalized user input.
    
    The vector store contains short bullet-style descriptions of tasks,
    tools, achievements, and project work.
    
    ### TASK
    Using the candidate profile, job description, and any personal notes
    from the user, generate **6–10 short retrieval queries**.
    
    Each query must:
    - be 6–12 words
    - point to concrete experience or achievements
    - support job responsibilities or required skills
    - reflect any specific themes the user wants included
    - avoid fluff, full sentences, or soft-skill language
    
    **Return the queries separated by new lines.***
    """
        ),
        HumanMessagePromptTemplate.from_template(
    ''' Generate multiple queries based on following Job descriptions: < {job_data} >,
        the cover letter is to be personalized based on -> custom user Input: < {user_personalized_input} >
    '''
        )
    ])

