from langchain_google_genai import GoogleGenerativeAIEmbeddings
from functools import lru_cache
from app.core.config import Settings
from typing import Optional



class GeminiEmbeddingsCustomDim(GoogleGenerativeAIEmbeddings):
    '''
    Class Wrapper for Google Vertex AI Embeddings
     - the original class's default dimension is 3072, which is too large for our use case
     - override the _prepare_request method to set dimension to custom_output_dimensionality
    '''
    # override pydantic fields for GoogleGenerativeAIEmbeddings
    custom_output_dimensionality: Optional[int] = None
    def __init__(self, output_dimensionality: Optional[int] = None, **kwargs):
        super().__init__(**kwargs)
        self.custom_output_dimensionality = output_dimensionality

    def _prepare_request(
        self,
        text: str,
        *,
        task_type: Optional[str] = None,
        title: Optional[str] = None,
        output_dimensionality: Optional[int] = None,
    ):
        ''' Overriding the _prepare_request method. to accept Dimensionality at class initialization.
        aim: set default output_dimensionality to custom_output_dimensionality if not provided in method call.
        '''

        if output_dimensionality is None:
            output_dimensionality = self.custom_output_dimensionality

        # call super or replicate logic
        return super()._prepare_request(
            text,
            task_type=task_type,
            title=title,
            output_dimensionality=output_dimensionality,
        )



@lru_cache()
def get_embedding_model():
    return GeminiEmbeddingsCustomDim(
        model="models/gemini-embedding-001",
        api_key=Settings.GOOGLE_API_KEY,
        task_type="RETRIEVAL_QUERY",
        output_dimensionality=Settings.QDRANT_DB_DIMENSION,
    )