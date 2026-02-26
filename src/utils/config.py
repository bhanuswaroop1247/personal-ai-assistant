import os
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

GEMINI_MODEL = "gemini-2.5-flash"


def load_api_key(key_from_ui: str = "") -> str:
    """Return the Gemini API key.

    Priority order:
      1. Value typed directly in the UI (key_from_ui)
      2. st.secrets (Streamlit Cloud)
      3. GEMINI_API_KEY environment variable
      4. .env file in the project root (loaded manually)

    Returns:
        The API key string, or empty string if not found.
    """
    # 1. UI input takes top priority
    if key_from_ui and key_from_ui.strip():
        return key_from_ui.strip()

    # 2. Streamlit Cloud secrets
    key = _load_from_streamlit_secrets("GEMINI_API_KEY")
    if key:
        return key

    # 3. Environment variable
    env_key = os.environ.get("GEMINI_API_KEY", "")
    if env_key:
        return env_key

    # 4. Manual .env file parse (no external dependency)
    env_file = _find_env_file()
    if env_file:
        key = _parse_env_file(env_file, "GEMINI_API_KEY")
        if key:
            return key

    return ""


def load_para_path(path_from_ui: str = "") -> str:
    """Return the PARA root path.

    Priority order:
      1. Value typed in the UI
      2. st.secrets (Streamlit Cloud)
      3. PARA_ROOT_PATH environment variable
      4. .env file

    Returns:
        The path string, or empty string if not found.
    """
    if path_from_ui and path_from_ui.strip():
        return path_from_ui.strip()

    path = _load_from_streamlit_secrets("PARA_ROOT_PATH")
    if path:
        return path

    env_path = os.environ.get("PARA_ROOT_PATH", "")
    if env_path:
        return env_path

    env_file = _find_env_file()
    if env_file:
        path = _parse_env_file(env_file, "PARA_ROOT_PATH")
        if path:
            return path

    return ""


def validate_api_key(api_key: str) -> tuple[bool, str]:
    """Basic validation of the API key format.

    Returns:
        (is_valid, error_message) tuple.
    """
    if not api_key or not api_key.strip():
        return False, "API key is missing. Please enter your Gemini API key."
    if len(api_key.strip()) < 20:
        return False, "API key looks too short. Please check it and try again."
    return True, ""


def validate_para_path(para_path: str) -> tuple[bool, str]:
    """Validate that the PARA root path exists and is a directory.

    Returns:
        (is_valid, error_message) tuple.
    """
    if not para_path or not para_path.strip():
        return False, "PARA path is missing. Please enter the path to your PARA folder."
    path = Path(para_path.strip())
    if not path.exists():
        return False, f"Directory not found: {para_path}\nPlease check the path and try again."
    if not path.is_dir():
        return False, f"Path is not a directory: {para_path}"
    return True, ""


def load_qdrant_url(url_from_ui: str = "") -> str:
    """Return the Qdrant Cloud URL.

    Priority: UI → st.secrets → env var → .env file
    """
    if url_from_ui and url_from_ui.strip():
        return url_from_ui.strip()
    url = _load_from_streamlit_secrets("QDRANT_URL")
    if url:
        return url
    env_val = os.environ.get("QDRANT_URL", "")
    if env_val:
        return env_val
    env_file = _find_env_file()
    if env_file:
        val = _parse_env_file(env_file, "QDRANT_URL")
        if val:
            return val
    return ""


def load_qdrant_api_key(key_from_ui: str = "") -> str:
    """Return the Qdrant API key.

    Priority: UI → st.secrets → env var → .env file
    """
    if key_from_ui and key_from_ui.strip():
        return key_from_ui.strip()
    key = _load_from_streamlit_secrets("QDRANT_API_KEY")
    if key:
        return key
    env_val = os.environ.get("QDRANT_API_KEY", "")
    if env_val:
        return env_val
    env_file = _find_env_file()
    if env_file:
        val = _parse_env_file(env_file, "QDRANT_API_KEY")
        if val:
            return val
    return ""


def validate_qdrant(url: str, api_key: str) -> tuple[bool, str]:
    """Basic format validation for Qdrant credentials (no network call)."""
    if not url or not url.strip():
        return False, "Qdrant URL is missing."
    if not url.strip().startswith("http"):
        return False, "Qdrant URL must start with http:// or https://"
    if not api_key or not api_key.strip():
        return False, "Qdrant API key is missing."
    return True, ""


# --- Internal helpers ---

def _load_from_streamlit_secrets(key: str) -> str:
    """Try to read a value from st.secrets (Streamlit Cloud).

    Returns empty string if streamlit is not running or key is absent.
    """
    try:
        import streamlit as st
        value = st.secrets.get(key, "")
        return str(value).strip() if value else ""
    except Exception:
        return ""


def _find_env_file() -> str:
    """Search for a .env file walking up from the current working directory."""
    current = Path.cwd()
    for directory in [current, *current.parents]:
        candidate = directory / ".env"
        if candidate.exists():
            return str(candidate)
    return ""


def _parse_env_file(filepath: str, key: str) -> str:
    """Parse a single key from a .env file without external libraries."""
    try:
        with open(filepath, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("#") or "=" not in line:
                    continue
                k, _, v = line.partition("=")
                if k.strip() == key:
                    return v.strip().strip('"').strip("'")
    except OSError as e:
        logger.warning("Could not read .env file %s: %s", filepath, e)
    return ""
