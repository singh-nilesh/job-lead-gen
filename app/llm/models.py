
from langchain_google_genai import ChatGoogleGenerativeAI
from app.core.config import Settings
from functools import lru_cache

@lru_cache()
def get_llm_model():
    ''' Get the LLM model instance for Google Gemini '''
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite",
        api_key=Settings.GOOGLE_API_KEY,
        temperature=0.2,
    )
    return llm