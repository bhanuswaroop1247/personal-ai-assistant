import os
import logging
import time
from pathlib import Path
from typing import List, Tuple

from models.data_models import ProjectInfo

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SUPPORTED_EXTENSIONS = {".md", ".txt"}
PARA_FOLDERS = ["Projects", "Areas", "Resources"]  # Archive skipped in MVP


def read_file(filepath: str) -> Tuple[str, bool]:
    """Read a file trying UTF-8 first, falling back to latin-1.

    Returns:
        (content, success) tuple. content is empty string on failure.
    """
    path = Path(filepath)
    for encoding in ("utf-8", "latin-1"):
        try:
            content = path.read_text(encoding=encoding)
            return content, True
        except UnicodeDecodeError:
            continue
        except OSError as e:
            logger.warning("Cannot read file %s: %s", filepath, e)
            return "", False
    logger.warning("Failed to decode file %s with any encoding", filepath)
    return "", False


def read_directory(path: str) -> List[str]:
    """Recursively scan a directory and return paths of supported files.

    Returns:
        List of absolute file path strings for .md and .txt files.
    """
    dir_path = Path(path)
    if not dir_path.exists():
        logger.warning("Directory does not exist: %s", path)
        return []
    if not dir_path.is_dir():
        logger.warning("Path is not a directory: %s", path)
        return []

    found_files: List[str] = []
    try:
        for item in dir_path.rglob("*"):
            if item.is_file() and item.suffix.lower() in SUPPORTED_EXTENSIONS:
                found_files.append(str(item))
    except PermissionError as e:
        logger.warning("Permission denied scanning %s: %s", path, e)

    return found_files


def _get_last_modified(path: str) -> float:
    """Return the most recent modification time among all files in a directory."""
    dir_path = Path(path)
    latest = 0.0
    try:
        for item in dir_path.rglob("*"):
            if item.is_file():
                mtime = item.stat().st_mtime
                if mtime > latest:
                    latest = mtime
    except OSError:
        pass
    return latest


def get_para_structure(root_path: str) -> Tuple[List[ProjectInfo], List[str]]:
    """Read the full PARA folder structure and return project info objects.

    Args:
        root_path: Path to the PARA root directory.

    Returns:
        (projects, warnings) where projects is a list of ProjectInfo sorted
        by last modified (newest first), and warnings is a list of issue strings.
    """
    warnings: List[str] = []
    root = Path(root_path)

    # Validate root exists
    if not root.exists():
        raise FileNotFoundError(f"PARA root directory not found: {root_path}")
    if not root.is_dir():
        raise NotADirectoryError(f"Path is not a directory: {root_path}")

    # Validate Projects/ folder exists (required)
    projects_path = root / "Projects"
    if not projects_path.exists():
        raise FileNotFoundError(
            f"'Projects' folder not found inside: {root_path}\n"
            "Please ensure your PARA structure has a 'Projects/' folder."
        )

    projects: List[ProjectInfo] = []

    # --- Read Projects/ (required, primary source) ---
    project_entries = sorted(projects_path.iterdir()) if projects_path.is_dir() else []
    if not project_entries:
        warnings.append("Projects/ folder exists but is empty.")

    for entry in project_entries:
        if entry.is_dir():
            files = read_directory(str(entry))
            if not files:
                warnings.append(f"Project folder '{entry.name}' has no readable files.")
                continue
            content_parts: List[str] = []
            read_ok = 0
            read_fail = 0
            for f in files:
                text, success = read_file(f)
                if success and text.strip():
                    rel = Path(f).name
                    content_parts.append(f"### {rel}\n{text.strip()}")
                    read_ok += 1
                else:
                    read_fail += 1
            if read_fail:
                warnings.append(
                    f"Project '{entry.name}': {read_fail} file(s) could not be read."
                )
            projects.append(ProjectInfo(
                name=entry.name,
                path=str(entry),
                files=[Path(f).name for f in files],
                content="\n\n".join(content_parts),
                last_modified=_get_last_modified(str(entry)),
                file_count=len(files),
            ))
        elif entry.is_file() and entry.suffix.lower() in SUPPORTED_EXTENSIONS:
            # Single-file project (file directly in Projects/)
            text, success = read_file(str(entry))
            if not success:
                warnings.append(f"Could not read project file: {entry.name}")
                continue
            projects.append(ProjectInfo(
                name=entry.stem,
                path=str(entry),
                files=[entry.name],
                content=text.strip(),
                last_modified=entry.stat().st_mtime,
                file_count=1,
            ))

    # Sort projects by last modified — newest first
    projects.sort(key=lambda p: p.last_modified, reverse=True)

    # --- Read Areas/ and Resources/ (optional, append as context) ---
    for folder_name in ["Areas", "Resources"]:
        folder_path = root / folder_name
        if not folder_path.exists():
            warnings.append(f"Optional folder '{folder_name}/' not found — skipping.")
            continue
        files = read_directory(str(folder_path))
        if not files:
            warnings.append(f"Optional folder '{folder_name}/' is empty — skipping.")

    return projects, warnings
