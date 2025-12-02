import os
import pytest_asyncio
from mongomock_motor import AsyncMongoMockClient
from qdrant_client import QdrantClient
from langchain_qdrant import QdrantVectorStore
from qdrant_client.http.models import VectorParams, Distance
from app.llm.embedding import get_embedding_model
from app.core.config import Settings

# set global test mode
os.environ.setdefault("MODE", "test")


@pytest_asyncio.fixture
async def app_db_mock():
    """ Fixture to provide a mock MongoDB database for testing """
    client = AsyncMongoMockClient()
    db = client["test_db"]
    yield db



@pytest_asyncio.fixture
async def vector_store_mock():
    """ Fixture to provide a mock QdrantVectorStore for testing """
    client = QdrantClient(":memory:", prefer_grpc=False)
    client.create_collection(
            collection_name="test",
            vectors_config=VectorParams(
                size=Settings.QDRANT_DB_DIMENSION,
                distance=Distance.COSINE,
            ),
        )
    
    # Langchain wrapper for Qdrant vector store
    vector_store = QdrantVectorStore(
        client=client,
        collection_name="test",

        # Using Google API, it is independent of app logic
        embedding=get_embedding_model(),
    )
    yield vector_store