"""Thin wrapper around Google gemini-embedding-001 for document/query embedding."""
import logging
from typing import List

import google.genai as genai
from google.genai import types as genai_types

logger = logging.getLogger(__name__)

EMBEDDING_MODEL = "models/gemini-embedding-001"
VECTOR_SIZE = 3072         # gemini-embedding-001 output dimension
MAX_EMBED_CHARS = 8_000    # safe character limit per chunk


def _truncate(text: str) -> str:
    return text[:MAX_EMBED_CHARS] if len(text) > MAX_EMBED_CHARS else text


def embed_text(client: genai.Client, text: str, task_type: str = "RETRIEVAL_DOCUMENT") -> List[float]:
    """Embed a single text. Returns list of 768 floats."""
    response = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=_truncate(text),
        config=genai_types.EmbedContentConfig(task_type=task_type),
    )
    return list(response.embeddings[0].values)


def embed_query(client: genai.Client, query: str) -> List[float]:
    """Embed a user query (RETRIEVAL_QUERY task type for better recall)."""
    return embed_text(client, query, task_type="RETRIEVAL_QUERY")


def embed_batch(client: genai.Client, texts: List[str], task_type: str = "RETRIEVAL_DOCUMENT") -> List[List[float]]:
    """Embed multiple texts in one API call. Returns list of 768-float vectors."""
    truncated = [_truncate(t) for t in texts]
    response = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=truncated,
        config=genai_types.EmbedContentConfig(task_type=task_type),
    )
    return [list(e.values) for e in response.embeddings]
