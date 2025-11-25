
''' Prompt for ingesting and parsing resumes using LLMs '''
from functools import lru_cache
from langchain.prompts import ChatPromptTemplate


prompt_template = """
  You are an expert resume generator.  
  You are an expert resume parser.

  Your task is to extract structured resume information from the provided raw resume text and output it using the schema defined in {format_instructions}.

  Rules:
  - Extract only information explicitly present in the resume input.
  - Light rewriting is allowed for grammar, clarity, and ATS-friendly phrasing.
  - Do NOT invent missing sections; set them to null.
  - professional_summary: Write a synthesized 80–100 word summary derived ONLY from available resume content.
  - Work experience: Rewrite into 3–5 action-oriented, impact-focused bullets per job.
  - Projects: Extract and rewrite into 2–4 concise bullets per project.
  - Education, skills, certifications, extracurriculars: Extract only if present; otherwise return null.
  - Avoid first-person language.
  - Maintain professional and consistent tone.

  Resume Input:
  {resume_input}

"""


@lru_cache()
def get_ingest_resume_prompt() -> ChatPromptTemplate:
    return ChatPromptTemplate(template=prompt_template)