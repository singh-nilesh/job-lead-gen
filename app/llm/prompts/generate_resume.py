''' Prompt template for generating resume content using LLM'''

from functools import lru_cache
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate


prompt_template = """
    You are an expert resume generator designed for candidate–job retrieval and resume tailoring systems.

    Your task is to produce clean, professional resume content following the Pydantic schema: {format_instructions}.

    *STEP 1 — PROFILE GENERATION*
    Create:
    - Full name
    - A professional summary of 80–100 words (ATS-optimized, concise, impact-focused)
    - Skills (4–7 high-signal technical skills, based on domains / categories), using this format: ["Programming: Python, SQL, MongoDB, NumPy, Flask","ML & Analytics: Feature engineering, clustering, regression, visualization"]

    *STEP 2 — EXPERIENCE & PROJECTS*
    If present, generate:
    - Work Experience (1–2 roles)  
      Each with 3–5 bullet points using action verbs, quantifiable outcomes, and technical depth.

    - Projects (2–3 strong projects)  
      Each with tech stack, optional link, date range, and 2–4 concise bullets describing problem, approach, and impact.

    If a section or attribute is not applicable, use null.

    *STEP 3 — EDUCATION & EXTRAS*
    Produce:
    - Education (1–2 entries, or null)  
    - Extra-curricular (1–2 entries with short bullet descriptions, or null)

    *CONTENT RULES*
    - Total text across all fields = *400–450 words*.
    - No first-person language.
    - No fluff; keep language professional and ATS-friendly.
    - Use null instead of empty lists/strings or None.
    - Make use of Context provided, don't fabricate details.
    - Can refine the phrasing, and structure for clarity and impact.
    - Make use of dates and numerical metrics, where applicable.

    Generate high-quality, realistic resume content suitable for technical job applications based on the provided user context.
    User Data:
    {user_data}
"""

@lru_cache()
def get_generate_resume_prompt() -> ChatPromptTemplate:
    return ChatPromptTemplate.from_messages([
        HumanMessagePromptTemplate.from_template(prompt_template)
    ])