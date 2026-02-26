"""Ingest PARA files into Qdrant: read → embed → upsert."""
import logging
import time
from pathlib import Path
from typing import Callable, List, Optional, Tuple

import google.genai as genai
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct

from agent.embedder import embed_batch
from agent.vector_store import ensure_collection, file_point_id, upsert_points
from utils.file_handler import read_directory, read_file

logger = logging.getLogger(__name__)

PARA_FOLDERS = ["Projects", "Areas", "Resources"]
BATCH_SIZE = 10      # files per embedding batch
BATCH_DELAY = 3.0    # seconds between batches (rate-limit headroom)
RATE_LIMIT_WAIT = 65 # seconds to wait on a 429 before retrying the batch


def ingest_para(
    para_root: str,
    gemini_api_key: str,
    qdrant_client: QdrantClient,
    force_reindex: bool = False,
    progress_callback: Optional[Callable[[str], None]] = None,
) -> Tuple[int, int, List[str]]:
    """Read all PARA files, embed them, and upsert to Qdrant.

    Args:
        para_root:          Path to the PARA root directory.
        gemini_api_key:     Google API key (used for text-embedding-004).
        qdrant_client:      Connected QdrantClient.
        force_reindex:      If True, wipe the collection first.
        progress_callback:  Optional callable(str) for live progress messages.

    Returns:
        (indexed, skipped, warnings)
    """
    from agent.vector_store import clear_and_reset  # avoid circular at module level

    def _log(msg: str) -> None:
        logger.info(msg)
        if progress_callback:
            progress_callback(msg)

    warnings: List[str] = []
    root = Path(para_root)

    if not root.exists():
        raise FileNotFoundError(f"PARA root not found: {para_root}")

    if force_reindex:
        _log("Force re-index: clearing existing collection…")
        clear_and_reset(qdrant_client)
    else:
        ensure_collection(qdrant_client)

    genai_client = genai.Client(api_key=gemini_api_key.strip())

    # ── Collect all files with their metadata ─────────────────────────────────
    file_records: List[dict] = []

    for folder_name in PARA_FOLDERS:
        folder_path = root / folder_name
        if not folder_path.exists():
            warnings.append(f"'{folder_name}/' not found — skipping.")
            continue

        files = read_directory(str(folder_path))
        if not files:
            warnings.append(f"'{folder_name}/' is empty — skipping.")
            continue

        _log(f"  Found {len(files)} file(s) in {folder_name}/")

        for file_path in files:
            text, success = read_file(file_path)
            if not success or not text.strip():
                continue

            p = Path(file_path)
            try:
                rel_parts = p.relative_to(root).parts
                para_folder = rel_parts[0]
                project_name = rel_parts[1] if len(rel_parts) > 2 else rel_parts[0]
            except ValueError:
                para_folder = folder_name
                project_name = p.parent.name

            try:
                last_modified = p.stat().st_mtime
            except OSError:
                last_modified = 0.0

            file_records.append({
                "file_path": str(p),
                "filename": p.name,
                "project_name": project_name,
                "para_folder": para_folder,
                "text": text.strip(),
                "last_modified": last_modified,
            })

    if not file_records:
        warnings.append("No readable files found in PARA folders.")
        return 0, 0, warnings

    _log(f"Embedding {len(file_records)} file(s) in batches of {BATCH_SIZE}…")

    # ── Embed in batches and upsert ───────────────────────────────────────────
    indexed = 0
    skipped = 0

    for batch_start in range(0, len(file_records), BATCH_SIZE):
        batch = file_records[batch_start: batch_start + BATCH_SIZE]
        texts = [r["text"] for r in batch]

        batch_num = batch_start // BATCH_SIZE + 1
        try:
            vectors = embed_batch(genai_client, texts, task_type="RETRIEVAL_DOCUMENT")
        except Exception as e:
            err_str = str(e)
            if "429" in err_str or "RESOURCE_EXHAUSTED" in err_str:
                _log(f"  Rate limit hit — waiting {RATE_LIMIT_WAIT}s before retrying batch {batch_num}…")
                time.sleep(RATE_LIMIT_WAIT)
                try:
                    vectors = embed_batch(genai_client, texts, task_type="RETRIEVAL_DOCUMENT")
                except Exception as retry_e:
                    warnings.append(f"Batch {batch_num} failed after retry: {retry_e}")
                    skipped += len(batch)
                    continue
            else:
                warnings.append(f"Embedding batch {batch_num} failed: {e}")
                skipped += len(batch)
                continue

        points: List[PointStruct] = []
        for record, vector in zip(batch, vectors):
            points.append(PointStruct(
                id=file_point_id(record["file_path"]),
                vector=vector,
                payload={
                    "text": record["text"][:8_000],
                    "filename": record["filename"],
                    "project_name": record["project_name"],
                    "para_folder": record["para_folder"],
                    "file_path": record["file_path"],
                    "last_modified": record["last_modified"],
                },
            ))

        upsert_points(qdrant_client, points)
        indexed += len(points)
        _log(f"  Indexed {indexed}/{len(file_records)} files…")

        if batch_start + BATCH_SIZE < len(file_records):
            time.sleep(BATCH_DELAY)

    _log(f"Indexing complete — {indexed} indexed, {skipped} skipped.")
    return indexed, skipped, warnings


def ingest_single_note(
    title: str,
    content: str,
    para_folder: str,
    gemini_api_key: str,
    qdrant_client: QdrantClient,
) -> bool:
    """Embed a single user-written note and upsert it into Qdrant.

    Args:
        title:           Note title (used as filename/identifier).
        content:         Note body text.
        para_folder:     One of: Projects, Areas, Resources, Archive.
        gemini_api_key:  Google API key for embedding.
        qdrant_client:   Connected QdrantClient.

    Returns:
        True if saved successfully, False on error.
    """
    from datetime import datetime as _dt
    from agent.embedder import embed_text

    try:
        ensure_collection(qdrant_client)
        genai_client = genai.Client(api_key=gemini_api_key.strip())
        vector = embed_text(genai_client, content, task_type="RETRIEVAL_DOCUMENT")

        note_id = file_point_id(f"user_note::{para_folder}::{title}")
        point = PointStruct(
            id=note_id,
            vector=vector,
            payload={
                "text": content[:8_000],
                "filename": title,
                "project_name": title,
                "para_folder": para_folder,
                "file_path": f"user_note/{para_folder}/{title}",
                "last_modified": _dt.now().timestamp(),
                "source": "user_note",
                "created_at": _dt.now().isoformat(),
            },
        )
        upsert_points(qdrant_client, [point])
        logger.info("Saved user note: %r in %s", title, para_folder)
        return True

    except Exception as e:
        logger.error("Failed to save note %r: %s", title, e)
        return False
