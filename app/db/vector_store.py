from functools import lru_cache
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from app.core.config import Settings, settings

from langchain_qdrant import QdrantVectorStore
from app.llm.embedding import GeminiEmbeddingsCustomDim

@lru_cache()
def get_client():
    ''' Returns the Qdrant client instance => client '''
    return  QdrantClient(
        url=Settings.QDRANT_URL,
        timeout=30,
    )

def ensure_collection_exists ():
    client = get_client()
    name = Settings.QDRANT_COLLECTION_NAME

    existing_coll = client.get_collection(name=name, ignore_missing=True)
    if existing_coll is None:

        # Create Vector store collection
        client.create_collection(
            collection_name=name,
            vectors_config= VectorParams(
                size= Settings.QDRANT_DB_DIMENSION,
                distance= Distance.COSINE
            )
        )

@lru_cache()
def get_embedding_model():
    return GeminiEmbeddingsCustomDim(
        model="models/gemini-embedding-001",
        task_type="RETRIEVAL_QUERY",
        output_dimensionality=Settings.QDRANT_DB_DIMENSION,
    )


# Langchain wrapper for Qdrant vector store
@lru_cache()
def get_vector_store() -> QdrantVectorStore:
    ''' Returns the main vector store instance => vector_store '''

    ensure_collection_exists()
    return QdrantVectorStore(
        client=get_client(),
        collection_name=Settings.QDRANT_COLLECTION_NAME,
        embeddings=get_embedding_model(),
    )
