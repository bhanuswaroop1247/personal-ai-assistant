# Python Tips & Best Practices

## Performance
- Use `pathlib.Path` over `os.path` for modern file handling
- Prefer dataclasses over dicts for structured data
- Use `rglob` for recursive directory walking

## Type hints
- Always annotate function signatures in production code
- Use `tuple[bool, str]` (Python 3.10+) over `Tuple[bool, str]`
- `from __future__ import annotations` for forward references

## Streamlit patterns
- Store heavy computation results in `st.session_state`
- Use `st.cache_data` for functions that read files
- `st.rerun()` to force a clean re-render after state changes

## Testing
- pytest fixtures over setUp/tearDown
- Use `tmp_path` fixture for file system tests
- `monkeypatch` for environment variable overrides

## Useful stdlib modules
- `pathlib` — file paths
- `dataclasses` — structured data
- `logging` — structured logging
- `json` — config and API responses
