import json
import logging
import time
from typing import Optional

import google.genai as genai
from google.genai import errors as genai_errors, types as genai_types

from models.data_models import Context, Recommendation
from utils.config import GEMINI_MODEL

logger = logging.getLogger(__name__)

# ── Prompt template ───────────────────────────────────────────────────────────

SYSTEM_ROLE = """You are Executa, an AI execution assistant.
Your role is to analyze a knowledge worker's PARA-structured knowledge base \
and recommend the single most valuable next action they should take right now."""

CHAIN_OF_THOUGHT_INSTRUCTIONS = """
Think step by step before giving your final answer:

Step 1 — List all active projects found in the Projects/ folder.
Step 2 — For each project identify: last activity signals, stated goals, and explicit next steps.
Step 3 — Assess priority for each project based on:
  - Urgency signals (deadlines, words like "urgent", "asap", "blocked", "due")
  - Dependencies or blockers that could delay progress
  - User constraints from their query (time available, energy level, focus type)
Step 4 — Identify the single highest-priority project.
Step 5 — Determine the most specific, immediately actionable next step for that project.
Step 6 — Explain clearly why this action is the most valuable thing to do right now.
"""

OUTPUT_FORMAT = """
Respond ONLY with a valid JSON object — no markdown fences, no extra text.
Use exactly this structure:

{
  "action": "<specific, immediately actionable next step — one clear sentence>",
  "project_name": "<name of the project this relates to>",
  "reasoning": "<full chain-of-thought explanation referencing the files and signals you found>",
  "files_consulted": ["<filename1>", "<filename2>"]
}

Constraints:
- Be specific — avoid vague advice like "work on your project"
- Cite the actual file names that informed your decision
- The action must be something the user can start doing within the next 5 minutes
- If two projects are equally urgent, explain the tie-breaking factor
"""


def _build_prompt(context: Context) -> str:
    """Assemble the full prompt from system role, CoT instructions, context, and query."""
    project_blocks = []
    for project in context.projects:
        block = f"### Project: {project.name}\n"
        block += f"Files: {', '.join(project.files)}\n\n"
        block += project.content if project.content else "(no readable content)"
        project_blocks.append(block)

    context_section = "\n\n---\n\n".join(project_blocks) if project_blocks else "(no projects found)"

    prompt = f"""{SYSTEM_ROLE}

{CHAIN_OF_THOUGHT_INSTRUCTIONS}

---
## YOUR KNOWLEDGE BASE CONTEXT

{context_section}

---
## USER QUERY

{context.user_query}

---
## YOUR RESPONSE

{OUTPUT_FORMAT}"""

    # Log truncated prompt for debugging
    logger.debug("Prompt (first 500 chars): %s", prompt[:500])
    return prompt


def _call_gemini(client: genai.Client, prompt: str) -> str:
    """Make a single Gemini API call and return the raw text response."""
    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
        config=genai_types.GenerateContentConfig(
            temperature=0.7,
            max_output_tokens=8192,
        ),
    )
    return response.text


def get_recommendation(context: Context, api_key: str) -> Recommendation:
    """Run the full reasoning pipeline: build prompt → call Gemini → return raw response.

    Retries once on transient failure before raising.

    Args:
        context:  Assembled Context object from context_builder.
        api_key:  Gemini API key.

    Returns:
        Recommendation with raw_response populated (parsing done by response_parser).

    Raises:
        ValueError:   Invalid API key or no projects in context.
        RuntimeError: API call failed after retry.
    """
    if not api_key or not api_key.strip():
        raise ValueError("Gemini API key is missing.")

    if not context.projects:
        raise ValueError("No projects found in context — nothing to analyse.")

    client = genai.Client(api_key=api_key.strip())
    prompt = _build_prompt(context)

    last_error: Optional[Exception] = None

    for attempt in range(1, 3):  # attempt 1, then retry once (attempt 2)
        try:
            logger.info("Gemini API call — attempt %d", attempt)
            raw_text = _call_gemini(client, prompt)
            logger.info("Gemini API call succeeded on attempt %d", attempt)
            return Recommendation(raw_response=raw_text)

        except genai_errors.ClientError as e:
            status = getattr(e, "status_code", None)

            # Rate limit — don't retry immediately, surface to user
            if status == 429:
                raise RuntimeError(
                    "Rate limit reached. Please wait a moment and try again."
                ) from e

            # Auth error — retrying won't help
            if status in (401, 403):
                raise RuntimeError(
                    "API key rejected by Google. Please check your Gemini API key."
                ) from e

            last_error = e
            logger.warning("ClientError on attempt %d: %s", attempt, e)

        except genai_errors.ServerError as e:
            last_error = e
            logger.warning("ServerError on attempt %d: %s", attempt, e)

        except OSError as e:
            # Network-level errors (no internet, DNS failure, connection refused)
            raise RuntimeError(
                "Network connection error. Please check your internet connection and try again."
            ) from e

        except Exception as e:
            # Catch httpx timeout/connect errors by inspecting the type name
            err_type = type(e).__name__.lower()
            if "timeout" in err_type or "connect" in err_type:
                raise RuntimeError(
                    "Request timed out. Please check your internet connection and try again."
                ) from e
            last_error = e
            logger.warning("Unexpected error on attempt %d: %s", attempt, e)

        # Wait before retry (only if we're going to retry)
        if attempt < 2:
            logger.info("Retrying in 2 seconds…")
            time.sleep(2)

    raise RuntimeError(
        f"Gemini API call failed after 2 attempts. Last error: {last_error}"
    )
