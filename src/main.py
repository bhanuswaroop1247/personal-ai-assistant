import sys
import streamlit as st
from datetime import datetime

sys.path.insert(0, "src")

from utils.config import (
    load_api_key, load_para_path, load_qdrant_url, load_qdrant_api_key,
    validate_api_key, validate_para_path, validate_qdrant,
)
from agent.vector_store import get_qdrant_client, get_document_count, save_note
from agent.ingestion import ingest_para
from agent.context_builder import build_context
from agent.reasoning_engine import get_recommendation
from agent.response_parser import parse_response

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Personal AI Execution Assistant",
    page_icon="🤖",
    layout="centered",
)

# ── Session state initialisation ──────────────────────────────────────────────
if "api_key" not in st.session_state:
    st.session_state.api_key = load_api_key()
if "para_path" not in st.session_state:
    st.session_state.para_path = load_para_path()
if "qdrant_url" not in st.session_state:
    st.session_state.qdrant_url = load_qdrant_url()
if "qdrant_api_key" not in st.session_state:
    st.session_state.qdrant_api_key = load_qdrant_api_key()
if "query" not in st.session_state:
    st.session_state.query = ""
if "recommendation" not in st.session_state:
    st.session_state.recommendation = None
if "context" not in st.session_state:
    st.session_state.context = None
if "warnings" not in st.session_state:
    st.session_state.warnings = []
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "error_msg" not in st.session_state:
    st.session_state.error_msg = ""
if "timestamp" not in st.session_state:
    st.session_state.timestamp = ""
if "indexed_count" not in st.session_state:
    st.session_state.indexed_count = 0

# ── Header ────────────────────────────────────────────────────────────────────
st.title("🤖 Personal AI Execution Assistant")
st.markdown("*AI-powered decision support for knowledge workers*")

st.markdown(
    "Ask it what to work on. "
    "It semantically searches your knowledge base, reasons about priorities, and returns one clear recommendation."
)
st.markdown("---")


# ── Sync Knowledge Base ───────────────────────────────────────────────────────
st.subheader("📂 Knowledge Base")

_resolved_qurl = st.session_state.qdrant_url
_resolved_qkey = st.session_state.qdrant_api_key

# Show current index stats
try:
    _qc = get_qdrant_client(_resolved_qurl, _resolved_qkey)
    _doc_count = get_document_count(_qc)
    if _doc_count > 0:
        st.caption(f"**{_doc_count} documents** currently indexed in Qdrant.")
    else:
        st.caption("No documents indexed yet — click **Sync Knowledge Base** to get started.")
except Exception:
    st.caption("Qdrant not connected — configure your credentials above.")

col_sync, col_reindex = st.columns([3, 2])
with col_sync:
    sync_btn = st.button(
        "🔄 Sync Knowledge Base", type="secondary", use_container_width=True,
        help="Embed and upsert all PARA files (existing points are overwritten by file path ID).",
    )
with col_reindex:
    reindex_btn = st.button(
        "🗑️ Force Re-index", type="secondary", use_container_width=True,
        help="Wipe the collection and re-index everything from scratch.",
    )

if sync_btn or reindex_btn:
    force = bool(reindex_btn)
    resolved_para = st.session_state.para_path
    resolved_key  = st.session_state.api_key
    resolved_qurl = st.session_state.qdrant_url
    resolved_qkey = st.session_state.qdrant_api_key

    key_ok,  key_err  = validate_api_key(resolved_key)
    path_ok, path_err = validate_para_path(resolved_para)
    q_ok,    q_err    = validate_qdrant(resolved_qurl, resolved_qkey)

    if not key_ok:
        st.error(f"**API Key error:** {key_err}")
    elif not path_ok:
        st.error(f"**PARA path error:** {path_err}")
    elif not q_ok:
        st.error(f"**Qdrant config error:** {q_err}")
    else:
        sync_status = st.status(
            "Re-indexing knowledge base…" if force else "Syncing knowledge base…",
            expanded=True,
        )
        try:
            with sync_status:
                qclient = get_qdrant_client(resolved_qurl, resolved_qkey)
                indexed, skipped, warns = ingest_para(
                    para_root=resolved_para,
                    gemini_api_key=resolved_key,
                    qdrant_client=qclient,
                    force_reindex=force,
                    progress_callback=lambda msg: sync_status.write(msg),
                )
                st.session_state.indexed_count  = indexed
                st.session_state.para_path      = resolved_para
                st.session_state.api_key         = resolved_key
                st.session_state.qdrant_url      = resolved_qurl
                st.session_state.qdrant_api_key  = resolved_qkey

                sync_status.update(
                    label=f"Done — {indexed} file(s) indexed, {skipped} skipped.",
                    state="complete",
                )
                if warns:
                    with st.expander(f"Sync notices ({len(warns)})", expanded=False):
                        for w in warns:
                            st.markdown(f"- {w}")
        except FileNotFoundError as e:
            sync_status.update(label="Error", state="error")
            st.error(f"**Folder not found:** {e}")
        except Exception as exc:
            sync_status.update(label="Error", state="error")
            st.error(f"**Sync failed:** {exc}")

st.markdown("---")

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab_agent, tab_notes = st.tabs(["🤖 Agent", "📝 Notes"])

# ══════════════════════════════════════════════════════════════════════════════
# AGENT TAB
# ══════════════════════════════════════════════════════════════════════════════
with tab_agent:

    # ── Query input ───────────────────────────────────────────────────────────
    st.subheader("What should you work on?")

    query = st.text_area(
        "Your question",
        value=st.session_state.query,
        height=110,
        placeholder=(
            "What should I work on right now?\n"
            "I have 30 minutes — what is the most valuable task?\n"
            "Which project needs the most attention today?\n"
            "I am feeling stuck — where should I start?"
        ),
        help="Ask in plain English. You can include context like available time or energy level.",
        label_visibility="collapsed",
    )

    col1, col2 = st.columns([4, 1])
    with col1:
        submit = st.button("🚀 Get Recommendation", type="primary", use_container_width=True)
    with col2:
        clear = st.button("Clear", type="secondary", use_container_width=True)

    if clear:
        st.session_state.query = ""
        st.session_state.recommendation = None
        st.session_state.context = None
        st.session_state.warnings = []
        st.session_state.submitted = False
        st.session_state.error_msg = ""
        st.session_state.timestamp = ""
        st.rerun()

    # ── Submit handler — full agent pipeline ──────────────────────────────────
    st.markdown("---")

    if submit:
        st.session_state.query = query
        st.session_state.submitted = True
        st.session_state.recommendation = None
        st.session_state.context = None
        st.session_state.warnings = []
        st.session_state.error_msg = ""

        resolved_para = st.session_state.para_path
        resolved_key  = st.session_state.api_key
        resolved_qurl = st.session_state.qdrant_url
        resolved_qkey = st.session_state.qdrant_api_key

        if not query.strip():
            st.session_state.error_msg = (
                "Please type a question before clicking Get Recommendation."
            )
        else:
            key_ok,  key_err  = validate_api_key(resolved_key)
            path_ok, path_err = validate_para_path(resolved_para)
            q_ok,    q_err    = validate_qdrant(resolved_qurl, resolved_qkey)

            if not key_ok:
                st.session_state.error_msg = (
                    f"**API Key missing or invalid:** {key_err}\n\n"
                    "Check that your GEMINI_API_KEY secret is set correctly."
                )
            elif not path_ok:
                st.session_state.error_msg = (
                    f"**PARA path error:** {path_err}\n\n"
                    "Check that your PARA_ROOT_PATH secret points to a valid directory."
                )
            elif not q_ok:
                st.session_state.error_msg = (
                    f"**Qdrant configuration error:** {q_err}\n\n"
                    "Check that your QDRANT_URL and QDRANT_API_KEY secrets are set correctly."
                )
            else:
                status = st.status("Analysing your knowledge base…", expanded=True)
                try:
                    with status:
                        st.write("🔍 Searching your knowledge base…")
                        qclient = get_qdrant_client(resolved_qurl, resolved_qkey)
                        context, warnings = build_context(
                            resolved_para, query.strip(), resolved_key, qclient
                        )
                        st.session_state.context  = context
                        st.session_state.warnings = warnings
                        st.session_state.para_path      = resolved_para
                        st.session_state.api_key         = resolved_key
                        st.session_state.qdrant_url      = resolved_qurl
                        st.session_state.qdrant_api_key  = resolved_qkey

                        if not context.projects:
                            st.session_state.error_msg = (
                                "**No relevant documents found.**\n\n"
                                "Make sure you have synced your knowledge base first "
                                "(click **Sync Knowledge Base** above)."
                            )
                            status.update(label="No documents found", state="error")
                        else:
                            st.write(f"🧠 Reasoning across {len(context.projects)} relevant project(s)…")
                            st.write("💡 Generating your recommendation…")
                            raw_rec = get_recommendation(context, resolved_key)
                            recommendation = parse_response(raw_rec.raw_response)

                            if "retry" in recommendation.action.lower() or not recommendation.project_name or recommendation.project_name == "Unknown project":
                                st.session_state.error_msg = (
                                    "**Could not parse the recommendation clearly.**\n\n"
                                    "The model returned an unexpected format. "
                                    "Please click **Get Recommendation** again to retry."
                                )
                                status.update(label="Parse error — please retry", state="error")
                            else:
                                st.session_state.recommendation = recommendation
                                st.session_state.timestamp = datetime.now().strftime("%H:%M:%S")
                                st.write("✅ Done!")
                                status.update(label="Recommendation ready", state="complete")

                except ValueError as e:
                    err = str(e)
                    if "api key" in err.lower():
                        st.session_state.error_msg = (
                            "**Gemini API key is missing.**\n\n"
                            "Check that your GEMINI_API_KEY secret is set correctly."
                        )
                    elif "no projects" in err.lower():
                        st.session_state.error_msg = (
                            "**No projects found** in your Projects/ folder.\n\n"
                            "Make sure your Projects/ folder contains at least one `.md` or `.txt` file."
                        )
                    else:
                        st.session_state.error_msg = f"**Configuration error:** {err}"
                    status.update(label="Error", state="error")

                except RuntimeError as e:
                    err = str(e)
                    if "rate limit" in err.lower():
                        st.session_state.error_msg = (
                            "**Rate limit reached.**\n\n"
                            "You have hit the Gemini API free-tier limit. "
                            "Please wait a minute and try again."
                        )
                    elif "api key rejected" in err.lower() or "key rejected" in err.lower():
                        st.session_state.error_msg = (
                            "**API key rejected by Google.**\n\n"
                            "Please check that your GEMINI_API_KEY secret is valid."
                        )
                    elif "timed out" in err.lower() or "timeout" in err.lower():
                        st.session_state.error_msg = (
                            "**Request timed out.**\n\n"
                            "The Gemini API did not respond in time. "
                            "Please try again — your knowledge base may be very large."
                        )
                    elif "network connection" in err.lower() or "internet" in err.lower():
                        st.session_state.error_msg = (
                            "**Network connection error.**\n\n"
                            "Could not reach the Gemini API. "
                            "Please check your internet connection and try again."
                        )
                    elif "failed after" in err.lower():
                        st.session_state.error_msg = (
                            "**API call failed after retrying.**\n\n"
                            "There may be a temporary issue with the Gemini API. "
                            "Please wait a moment and try again."
                        )
                    else:
                        st.session_state.error_msg = f"**API error:** {err}\n\nPlease try again."
                    status.update(label="Error", state="error")

                except FileNotFoundError as e:
                    st.session_state.error_msg = (
                        f"**Folder not found:** {e}\n\n"
                        "Check that the path is correct and the folder exists."
                    )
                    status.update(label="Error", state="error")

                except Exception as e:
                    st.session_state.error_msg = (
                        f"**An unexpected error occurred:** `{type(e).__name__}: {e}`\n\n"
                        "Please try again. If the problem persists, "
                        "check your PARA folder permissions and API key."
                    )
                    status.update(label="Error", state="error")

    # ── Results area ──────────────────────────────────────────────────────────
    if not st.session_state.submitted:
        st.markdown("#### Getting started")
        st.markdown(
            "1. Click **🔄 Sync Knowledge Base** above to index your files into Qdrant\n"
            "2. Type your question and click **Get Recommendation**"
        )

    elif st.session_state.error_msg:
        st.error(st.session_state.error_msg)

    elif st.session_state.recommendation:
        rec   = st.session_state.recommendation
        ctx   = st.session_state.context
        warns = st.session_state.warnings

        st.subheader("Recommended Action")
        st.info(f"**{rec.action}**")

        st.markdown(f"**Project:** {rec.project_name}")
        st.markdown("")

        with st.expander("💡 Why this recommendation?", expanded=True):
            st.markdown(rec.reasoning)

        with st.expander("📚 Files consulted", expanded=False):
            if rec.citations:
                for f in rec.citations:
                    st.markdown(f"- `{f}`")
            else:
                st.markdown("*No specific files cited in this response.*")

        if warns:
            with st.expander(f"Notices ({len(warns)})", expanded=False):
                for w in warns:
                    st.markdown(f"- {w}")

        st.markdown("---")
        project_count  = len(ctx.projects) if ctx else 0
        qdrant_results = ctx.metadata.get("qdrant_results", 0) if ctx else 0
        doc_count      = ctx.metadata.get("qdrant_doc_count", 0) if ctx else 0
        st.caption(
            f"Generated at {st.session_state.timestamp}  ·  "
            f"{project_count} project(s) retrieved  ·  "
            f"{qdrant_results} chunks searched  ·  "
            f"{doc_count} total docs in index"
        )

# ══════════════════════════════════════════════════════════════════════════════
# NOTES TAB
# ══════════════════════════════════════════════════════════════════════════════
with tab_notes:

    st.subheader("Create a New Note")
    st.caption("Write a note and save it directly into your knowledge base — instantly searchable by the agent.")

    note_title = st.text_input(
        "Note Title",
        placeholder="e.g. Project Alpha meeting notes",
        key="note_title_input",
    )

    col_folder, col_space = st.columns([2, 3])
    with col_folder:
        note_folder = st.selectbox(
            "Save to",
            ["Projects", "Areas", "Resources", "Archive"],
            key="note_folder_input",
        )

    note_body = st.text_area(
        "Note",
        placeholder="Write your note here...",
        height=400,
        key="note_body_input",
        label_visibility="collapsed",
    )

    save_btn = st.button("💾 Save Note", type="primary")

    if save_btn:
        if not note_title.strip():
            st.warning("Please enter a note title before saving.")
        elif not note_body.strip():
            st.warning("Please write something in the note before saving.")
        else:
            resolved_key  = st.session_state.api_key
            resolved_qurl = st.session_state.qdrant_url
            resolved_qkey = st.session_state.qdrant_api_key

            with st.spinner("💾 Saving and indexing your note..."):
                qclient = get_qdrant_client(resolved_qurl, resolved_qkey)
                success = save_note(
                    note_title.strip(),
                    note_body.strip(),
                    note_folder,
                    resolved_key,
                    qclient,
                )

            if success:
                st.success("✅ Note saved and indexed! It's now searchable by the agent.")
            else:
                st.error("❌ Failed to save note. Please check your Qdrant connection.")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.caption("Personal AI Execution Assistant · Powered by Google Gemini + Qdrant · Python 3.13")
