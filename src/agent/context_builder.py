"""Build Context from Qdrant semantic search results."""
import logging
from collections import defaultdict
from typing import Dict, List, Tuple

import google.genai as genai
from qdrant_client import QdrantClient

from agent.embedder import embed_query
from agent.vector_store import get_document_count, search_similar
from models.data_models import Context, ProjectInfo

logger = logging.getLogger(__name__)

TOP_K = 15  # retrieve top-15 most semantically relevant file chunks

# Priority order for PARA folders in context assembly
_FOLDER_PRIORITY: Dict[str, int] = {"Projects": 0, "Areas": 1, "Resources": 2}


def build_context(
    para_root: str,
    user_query: str,
    gemini_api_key: str,
    qdrant_client: QdrantClient,
    top_k: int = TOP_K,
) -> Tuple[Context, List[str]]:
    """Assemble Context via semantic search in Qdrant.

    Pipeline:
      1. Check Qdrant collection is not empty
      2. Embed user query with RETRIEVAL_QUERY task type
      3. Search Qdrant for top_k most relevant documents
      4. Group results by project, build ProjectInfo objects
      5. Sort: Projects first, then Areas/Resources; newest first within each folder

    Args:
        para_root:       PARA root path (for informational metadata only).
        user_query:      The user's natural language question.
        gemini_api_key:  Google API key for query embedding.
        qdrant_client:   Connected QdrantClient.
        top_k:           Number of documents to retrieve.

    Returns:
        (Context, warnings)
    """
    warnings: List[str] = []

    # ── 1. Guard: collection must have documents ───────────────────────────────
    doc_count = get_document_count(qdrant_client)
    if doc_count == 0:
        warnings.append(
            "Qdrant collection is empty — click 'Sync Knowledge Base' to index your files first."
        )
        return Context(user_query=user_query), warnings

    # ── 2. Embed user query ────────────────────────────────────────────────────
    genai_client = genai.Client(api_key=gemini_api_key.strip())
    query_vector = embed_query(genai_client, user_query)

    # ── 3. Semantic search ─────────────────────────────────────────────────────
    results = search_similar(qdrant_client, query_vector, top_k=top_k)

    if not results:
        warnings.append("No relevant documents found for your query. Try rephrasing.")
        return Context(user_query=user_query), warnings

    logger.info("Qdrant search returned %d results (top_k=%d)", len(results), top_k)

    # ── 4. Group hits by project ───────────────────────────────────────────────
    project_chunks: Dict[str, List[dict]] = defaultdict(list)
    project_folder: Dict[str, str] = {}
    project_mtime: Dict[str, float] = {}

    for hit in results:
        payload = hit.payload or {}
        pname = payload.get("project_name", "Unknown")
        project_chunks[pname].append(payload)

        if pname not in project_folder:
            project_folder[pname] = payload.get("para_folder", "")
            project_mtime[pname] = payload.get("last_modified", 0.0)
        else:
            # Track most recent mtime across chunks of the same project
            mtime = payload.get("last_modified", 0.0)
            if mtime > project_mtime[pname]:
                project_mtime[pname] = mtime

    # ── 5. Build ProjectInfo objects ───────────────────────────────────────────
    projects: List[ProjectInfo] = []
    total_files = 0

    for pname, chunks in project_chunks.items():
        files = [c.get("filename", "") for c in chunks if c.get("filename")]
        content_parts = []
        for chunk in chunks:
            fname = chunk.get("filename", "")
            text = chunk.get("text", "")
            if fname and text:
                content_parts.append(f"### {fname}\n{text}")

        projects.append(ProjectInfo(
            name=pname,
            path=chunks[0].get("file_path", ""),
            files=files,
            content="\n\n".join(content_parts),
            last_modified=project_mtime[pname],
            file_count=len(files),
        ))
        total_files += len(files)

    # Sort: Projects folder first, then by recency within folder
    projects.sort(key=lambda p: (
        _FOLDER_PRIORITY.get(project_folder.get(p.name, ""), 9),
        -project_mtime.get(p.name, 0.0),
    ))

    context = Context(
        projects=projects,
        user_query=user_query,
        total_files_read=total_files,
        metadata={
            "para_root": para_root,
            "qdrant_results": len(results),
            "qdrant_doc_count": doc_count,
            "project_count": len(projects),
        },
    )

    logger.info(
        "Context built — %d project(s), %d file chunks from %d Qdrant results",
        len(projects), total_files, len(results),
    )
    return context, warnings
