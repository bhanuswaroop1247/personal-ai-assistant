import json
import logging
import re
from typing import Any, Dict, Optional

from models.data_models import Recommendation

logger = logging.getLogger(__name__)

REQUIRED_FIELDS = {"action", "project_name", "reasoning", "files_consulted"}


def _extract_json_block(text: str) -> Optional[str]:
    """Find and return the first JSON object in a string.

    Handles three common Gemini response formats:
      1. Pure JSON (no wrapper)
      2. JSON inside ```json ... ``` fences
      3. JSON embedded somewhere inside a longer text response
    """
    text = text.strip()

    # Format 1 — already a clean JSON object
    if text.startswith("{"):
        return text

    # Format 2 — fenced code block  ```json { ... } ```
    # Use greedy matching so we capture the full JSON object, not the first closing brace
    fence_match = re.search(r"```(?:json)?\s*(\{.*\})\s*```", text, re.DOTALL)
    if fence_match:
        return fence_match.group(1)

    # Format 3 — JSON object embedded anywhere in the text
    brace_match = re.search(r"\{.*\}", text, re.DOTALL)
    if brace_match:
        return brace_match.group(0)

    return None


def _validate_fields(data: Dict[str, Any]) -> Recommendation:
    """Validate required fields and return a populated Recommendation.

    Missing fields get sensible placeholder values rather than hard failures,
    so the user always sees something useful.
    """
    missing = REQUIRED_FIELDS - data.keys()
    if missing:
        logger.warning("Gemini response missing fields: %s", missing)

    action = str(data.get("action", "")).strip()
    project_name = str(data.get("project_name", "")).strip()
    reasoning = str(data.get("reasoning", "")).strip()
    files_consulted = data.get("files_consulted", [])

    # Normalise files_consulted to a list of strings
    if isinstance(files_consulted, str):
        files_consulted = [f.strip() for f in files_consulted.split(",") if f.strip()]
    elif isinstance(files_consulted, list):
        files_consulted = [str(f).strip() for f in files_consulted if str(f).strip()]
    else:
        files_consulted = []

    # Fill placeholders for any missing critical fields
    if not action:
        action = "Could not determine a specific action — please retry."
    if not project_name:
        project_name = "Unknown project"
    if not reasoning:
        reasoning = "Reasoning not available in this response."

    return Recommendation(
        action=action,
        project_name=project_name,
        reasoning=reasoning,
        citations=files_consulted,
    )


def _fallback_text_parse(raw: str) -> Recommendation:
    """Last-resort parser: extract meaning from plain text when JSON fails entirely.

    Looks for labelled lines like 'action:', 'project:', 'reasoning:' etc.
    """
    logger.warning("Falling back to plain-text parsing")
    data: Dict[str, Any] = {}

    patterns = {
        "action":        r"(?:action|next action|recommended action)\s*[:：]\s*(.+)",
        "project_name":  r"(?:project|project name)\s*[:：]\s*(.+)",
        "reasoning":     r"(?:reasoning|reason|rationale|explanation)\s*[:：]\s*(.+)",
        "files_consulted": r"(?:files?|sources?|citations?)\s*[:：]\s*(.+)",
    }

    for field, pattern in patterns.items():
        match = re.search(pattern, raw, re.IGNORECASE | re.DOTALL)
        if match:
            data[field] = match.group(1).strip()

    # If we found nothing useful, use the full raw text as reasoning
    if not data:
        data["reasoning"] = raw.strip()
        data["action"] = "Please retry — response format was unexpected."

    return _validate_fields(data)


def parse_response(raw_response: str) -> Recommendation:
    """Parse Gemini's raw text into a structured Recommendation.

    Strategy:
      1. Try to extract a JSON block from the response
      2. Try to parse it as JSON
      3. Validate all required fields
      4. Fall back to plain-text parsing if JSON fails

    Args:
        raw_response: The raw text returned by the Gemini API.

    Returns:
        Populated Recommendation dataclass. Never raises — always returns something.
    """
    if not raw_response or not raw_response.strip():
        logger.warning("Empty response from Gemini")
        return Recommendation(
            action="Empty response received — please retry.",
            reasoning="The model returned an empty response.",
        )

    # Attach raw response for debugging
    rec = None

    # ── Attempt JSON parsing ──────────────────────────────────────────────────
    json_str = _extract_json_block(raw_response)
    if json_str:
        try:
            data = json.loads(json_str)
            if isinstance(data, dict):
                rec = _validate_fields(data)
                logger.info("JSON parsing succeeded")
            else:
                logger.warning("JSON parsed but top-level is not a dict: %s", type(data))
        except json.JSONDecodeError as e:
            logger.warning("JSON decode failed: %s", e)

    # ── Fallback to text parsing ──────────────────────────────────────────────
    if rec is None:
        rec = _fallback_text_parse(raw_response)

    rec.raw_response = raw_response
    return rec
