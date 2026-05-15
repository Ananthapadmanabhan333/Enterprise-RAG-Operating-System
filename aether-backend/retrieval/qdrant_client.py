import os
from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams, Distance
import logging

logger = logging.getLogger(__name__)

QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
COLLECTION_NAME = "aether_knowledge"

try:
    client = QdrantClient(url=QDRANT_URL)
    # Ensure collection exists for deployable out-of-the-box experience
    if not client.collection_exists(COLLECTION_NAME):
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
        )
        logger.info(f"Created Qdrant collection: {COLLECTION_NAME}")
except Exception as e:
    logger.warning(f"Could not connect to Qdrant at startup: {e}")
    client = None

def mock_search_if_empty(query: str):
    return [
        {"id": "c1", "content": f"AetherOS securely ingests enterprise data. Query context: {query}", "score": 0.95},
        {"id": "c2", "content": "LangGraph orchestrates the retrieval multi-agent loops.", "score": 0.88}
    ]

async def hybrid_search(query: str, filters: dict, limit: int = 5):
    """
    Connects to Qdrant. If empty or disconnected, falls back to a mock 
    so the system remains runnable during demonstrations without ingestion.
    """
    if client is None:
        return mock_search_if_empty(query)
        
    try:
        from langchain_openai import OpenAIEmbeddings
        embeddings = OpenAIEmbeddings()
        vector = embeddings.embed_query(query)
        
        results = client.search(
            collection_name=COLLECTION_NAME,
            query_vector=vector,
            limit=limit
        )
        if not results:
            return mock_search_if_empty(query)
            
        return [
            {"id": res.id, "content": res.payload.get("page_content", ""), "score": res.score} 
            for res in results
        ]
    except Exception as e:
        logger.error(f"Search failed: {e}")
        return mock_search_if_empty(query)
