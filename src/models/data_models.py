from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class ProjectInfo:
    """Represents a single PARA project with its files and content."""
    name: str
    path: str
    files: List[str] = field(default_factory=list)
    content: str = ""
    last_modified: float = 0.0
    file_count: int = 0


@dataclass
class Context:
    """Aggregated context built from the PARA knowledge base."""
    projects: List[ProjectInfo] = field(default_factory=list)
    user_query: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    total_files_read: int = 0
    total_files_skipped: int = 0


@dataclass
class Recommendation:
    """Structured output from the reasoning engine."""
    action: str = ""
    project_name: str = ""
    reasoning: str = ""
    citations: List[str] = field(default_factory=list)
    raw_response: str = ""
