''' Prompt template for generating resume content using LLM'''

from functools import lru_cache
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate


prompt_template = """
    You are an expert resume generator designed for candidate–job retrieval and resume tailoring systems.

    Your task is to produce clean, professional resume content following the Pydantic schema: {format_instructions}.

    *STEP 1 — PROFILE GENERATION*
    Create:
    - Full name
    - Designation line (singel line, seprated by |, eg "Data Scientist | ML Engineer | Python Developer")
    - A professional summary of 60–80 words (ATS-optimized, concise, impact-focused)
    - Skills (4–7 high-signal technical skills) eg. "Programming: Python, SQL, MongoDB, NumPy, Flask","ML & Analytics: Feature engineering, clustering, regression, visualization"

    *STEP 2 — EXPERIENCE & PROJECTS*
    If present, generate:
    - Work Experience (1–2 roles)  
      Each with 3–5 bullet points using action verbs, quantifiable outcomes, and technical depth.

    - Projects (2–3 strong projects)  
      Each with tech stack, optional link, date range, and 2–4 concise bullets describing problem, approach, and impact.

    If a section has insufficient content, return `null`.

    *STEP 3 — EDUCATION & EXTRAS*
    Produce:
    - Education (1–2 entries, or null)  
    - Extra-curricular (1–2 entries with short bullet descriptions, or null)

    *CONTENT RULES*
    - Total text across all fields = **350–400 words**.
    - No first-person language.
    - No fluff; keep language professional and ATS-friendly.
    - Use null instead of empty lists/strings.
    - All bullets must be concise, meaningful, and high-signal.

    Generate high-quality, realistic resume content suitable for technical job applications based on the provided user context.
    User Data:
    {user_data}
"""

@lru_cache()
def get_generate_resume_prompt() -> ChatPromptTemplate:
    return ChatPromptTemplate.from_messages([
        HumanMessagePromptTemplate.from_template(prompt_template)
    ])