
from langchain_google_genai import ChatGoogleGenerativeAI
from functools import lru_cache

@lru_cache()
def get_llm_model():
    ''' Get the LLM model instance for Google Gemini '''
    llm = ChatGoogleGenerativeAI(
        model="models/gemini-1.5-chat",
        temperature=0.2,
    )
    return llm