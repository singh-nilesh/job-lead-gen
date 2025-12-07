''' Prompt to generate query strings for vector DB retrieval '''
from functools import lru_cache
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate

@lru_cache
def get_generate_coverletter_prompt():
    return ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(
            """You are an expert cover letter writer.
    Your job is to generate a polished, concise, and personalized cover letter based strictly on the given user profile data, job description, and personalization parameters.

    Follow these rules:
    - Content must be ATS-friendly, professional, and action-oriented.
    - Use a confident tone, avoid generic clichés, and always customize to the job.
    - Keep paragraphs compact (2–4 lines each).
    - Mention user achievements only if provided — no hallucinations.
    - If data is missing, gracefully skip that point.
    - DO NOT invent facts.
    Output MUST strictly follow the provided Pydantic structure: {format_instructions}
    """
        ),
        HumanMessagePromptTemplate.from_template(
            """ generate cover letter for the following job details: {job_data}
    based on given User Context:{user_context}.
    give the resume a personalized touch, by following {personalization_instructions}
    """
        )
    ])