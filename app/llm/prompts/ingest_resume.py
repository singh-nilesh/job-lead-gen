
''' Prompt for ingesting and parsing resumes using LLMs '''
from functools import lru_cache
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate


@lru_cache()
def get_ingest_resume_prompt() -> ChatPromptTemplate:
    return ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(
            """
    You are an expert resume generator.  
    You are an expert resume parser.

   Your task is to extract structured resume information from the provided raw resume text and output it using the output schema.

   Rules:
    - Extract only information explicitly present in the resume input.
    - Light rewriting is allowed for grammar, clarity, and ATS-friendly phrasing.
    - Do NOT invent missing sections; set them to null.
    - professional_summary: Write a synthesized 100-200 word summary derived ONLY from available resume content.
    - Work experience: Rewrite into 3–5 action-oriented, impact-focused bullets per job.
    - Projects: Extract and rewrite into 2–4 concise bullets per project.
    - Education, skills, certifications, extracurriculars: Extract only if present; otherwise return null.
    - Avoid first-person language.
    - Maintain professional and consistent tone.

   follow the output schema: {format_instructions}.

   Resume Content:
    {resume_input}
    """),
      HumanMessagePromptTemplate.from_template(
          " Ingest the following resume content: {resume_input}"
      )
    ])
