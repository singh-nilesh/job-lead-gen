from functools import lru_cache
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from app.core.config import Settings

from langchain_qdrant import QdrantVectorStore
from app.llm.embedding import get_embedding_model
from app.core.logger import db_logger as logger

@lru_cache()
def get_client():
    ''' Returns the Qdrant client instance => client '''
    try:
        client = QdrantClient(
            url=Settings.QDRANT_URL,
            timeout=30,
            prefer_grpc=False,
        )
        logger.info("Qdrant client created")
        return client
    except Exception as e:
        logger.error("Failed to create Qdrant client: %s", e)
        raise

def ensure_collection_exists ():
    client = get_client()
    name = Settings.QDRANT_COLLECTION_NAME

    try:
        client.get_collection(name)
        logger.info("Qdrant collection '%s' already exists", name)
    except Exception:
        logger.warning("Qdrant collection '%s' does not exist. Creating...", name)
        
        client.create_collection(
            collection_name=name,
            vectors_config=VectorParams(
                size=Settings.QDRANT_DB_DIMENSION,
                distance=Distance.COSINE,
            ),
        )
        logger.info("Qdrant collection '%s' created", name)


# Langchain wrapper for Qdrant vector store
@lru_cache()
def get_vector_store() -> QdrantVectorStore:
    ''' Returns the main vector store instance => vector_store '''
    try:
        ensure_collection_exists()
        vs = QdrantVectorStore(
            client=get_client(),
            collection_name=Settings.QDRANT_COLLECTION_NAME,
            embedding=get_embedding_model(),
        )
        logger.info("QdrantVectorStore initialized for collection: %s", Settings.QDRANT_COLLECTION_NAME)
        return vs
    except Exception as e:
        logger.error("Failed to initialize QdrantVectorStore for %s: %s", Settings.QDRANT_COLLECTION_NAME, e)
        raise
