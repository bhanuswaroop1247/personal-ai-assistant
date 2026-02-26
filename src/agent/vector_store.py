"""Qdrant operations for the PARA knowledge base."""
import logging
import uuid
from typing import Any, Dict, List, Optional

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    PointStruct,
    ScoredPoint,
    VectorParams,
)

from agent.embedder import VECTOR_SIZE

logger = logging.getLogger(__name__)

COLLECTION_NAME = "para_knowledge_base"


def get_qdrant_client(url: str, api_key: str) -> QdrantClient:
    return QdrantClient(url=url.strip(), api_key=api_key.strip())


def ensure_collection(client: QdrantClient) -> None:
    """Create the collection if it does not already exist."""
    existing = {c.name for c in client.get_collections().collections}
    if COLLECTION_NAME not in existing:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE),
        )
        logger.info("Created Qdrant collection: %s", COLLECTION_NAME)
    else:
        logger.debug("Collection already exists: %s", COLLECTION_NAME)


def file_point_id(file_path: str) -> str:
    """Deterministic UUID from file path — ensures idempotent upserts."""
    return str(uuid.uuid5(uuid.NAMESPACE_URL, file_path))


def upsert_points(client: QdrantClient, points: List[PointStruct]) -> None:
    if not points:
        return
    client.upsert(collection_name=COLLECTION_NAME, points=points, wait=True)
    logger.info("Upserted %d points", len(points))


def search_similar(
    client: QdrantClient,
    query_vector: List[float],
    top_k: int = 15,
) -> List[ScoredPoint]:
    """Return top_k most similar documents to the query vector."""
    return client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        limit=top_k,
        with_payload=True,
    )


def get_document_count(client: QdrantClient) -> int:
    """Return number of indexed documents (0 if collection missing)."""
    try:
        info = client.get_collection(COLLECTION_NAME)
        return info.points_count or 0
    except Exception:
        return 0


def save_note(
    title: str,
    content: str,
    para_folder: str,
    gemini_api_key: str,
    qdrant_client: QdrantClient,
) -> bool:
    """Embed and store a user-written note in Qdrant.

    Thin wrapper around ingest_single_note — keeps vector_store as the
    single public API surface for note writes.

    Returns:
        True if saved successfully, False on error.
    """
    from agent.ingestion import ingest_single_note
    return ingest_single_note(title, content, para_folder, gemini_api_key, qdrant_client)


def clear_and_reset(client: QdrantClient) -> None:
    """Delete all points by deleting and recreating the collection."""
    existing = {c.name for c in client.get_collections().collections}
    if COLLECTION_NAME in existing:
        client.delete_collection(COLLECTION_NAME)
        logger.info("Deleted collection: %s", COLLECTION_NAME)
    ensure_collection(client)
