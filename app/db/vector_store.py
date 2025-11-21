from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from app.core.config import Settings, settings



client = QdrantClient(
    url=Settings.QDRANT_URL,
    timeout=30,
)

# Create Vector store collection
client.create_collection(
    collection_name=Settings.QDRANT_COLLECTION_NAME,
    vectors_config= VectorParams(
        size= Settings.QDRANT_DB_DIMENSION,
        distance= Distance.COSINE
    )
)





def get_qdrant_client():
    pass
