# Executa

An AI execution assistant that reads your [PARA](https://fortelabs.com/blog/para/)-structured knowledge base, indexes it semantically with Qdrant, and uses Google Gemini to recommend your single most valuable next action.

## Features

- **Agent tab** — Ask "What should I work on?" and get a chain-of-thought recommendation grounded in your actual notes
- **Notes tab** — Write notes directly in the app; they're instantly embedded and searchable by the agent
- **Semantic search** — Powered by Qdrant Cloud vector DB (gemini-embedding-001, 3072-dim)
- **PARA-aware** — Understands Projects / Areas / Resources folder structure; prioritises active projects

## Tech Stack

| Layer | Technology |
|-------|-----------|
| UI | Streamlit |
| LLM | Google Gemini 2.5 Flash |
| Embeddings | gemini-embedding-001 (3072-dim) |
| Vector DB | Qdrant Cloud |
| Language | Python 3.13 |

## Local Setup

### 1. Clone and install

```bash
git clone https://github.com/bhanuswaroop1247/personal-ai-assistant.git
cd personal-ai-assistant
python -m venv venv
source venv/Scripts/activate   # Windows
# source venv/bin/activate     # Mac/Linux
pip install -r requirements.txt
```

### 2. Create `.env`

```env
GEMINI_API_KEY=your_gemini_api_key
PARA_ROOT_PATH=C:/path/to/your/PARA/folder
QDRANT_URL=https://your-cluster.qdrant.io
QDRANT_API_KEY=your_qdrant_api_key
```

Get a free Gemini API key at [aistudio.google.com](https://aistudio.google.com).
Get a free Qdrant Cloud cluster at [cloud.qdrant.io](https://cloud.qdrant.io).

### 3. Run

```bash
streamlit run src/main.py
```

Open http://localhost:8501, click **Sync Knowledge Base**, then ask the agent anything.

## Streamlit Cloud Deployment

1. Fork / push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io) → **New app**
3. Select repo, set **Main file path** to `src/main.py`
4. Add secrets in the dashboard (Settings → Secrets):

```toml
GEMINI_API_KEY = "..."
QDRANT_URL = "..."
QDRANT_API_KEY = "..."
```

> Note: `PARA_ROOT_PATH` is not needed on Cloud — users enter it directly in the app UI.

## PARA Folder Structure

The app expects this layout (Archive is intentionally skipped):

```
your-para-root/
  Projects/   ← active projects (.md or .txt files)
  Areas/      ← ongoing responsibilities
  Resources/  ← reference material
  Archive/    ← (skipped)
```

## License

MIT
