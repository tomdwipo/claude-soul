import os

from pydantic import BaseModel

_DEFAULT_EXT = (
    ".py,.js,.jsx,.ts,.tsx,.go,.rs,.rb,.php,.java,.kt,.kts,.scala,.swift,"
    ".c,.h,.cpp,.hpp,.cs,.sh,.gradle,.md,.rst,.txt,.xml,.yaml,.yml,.toml,.json"
)
_DEFAULT_EXCLUDE = "build,.git,.gradle,node_modules,.idea,dist,target,out,vendor,.venv,venv,__pycache__,.next,.mypy_cache,.pytest_cache"


def _csv(name: str, default: str) -> tuple:
    return tuple(x.strip() for x in os.getenv(name, default).split(",") if x.strip())


class Config(BaseModel):
    ollama_url: str = os.getenv("OLLAMA_URL", "http://host.docker.internal:11434")
    embed_model: str = os.getenv("EMBED_MODEL", "qwen3-embedding:0.6b")
    dense_dim: int = int(os.getenv("DENSE_DIM", "1024"))
    qdrant_url: str = os.getenv("QDRANT_URL", "http://qdrant:6333")
    collection: str = os.getenv("COLLECTION", "code_rag")
    repo_root: str = os.getenv("REPO_ROOT", "/repo")
    include_ext: tuple = _csv("INCLUDE_EXT", _DEFAULT_EXT)
    exclude_dirs: tuple = _csv("EXCLUDE_DIRS", _DEFAULT_EXCLUDE)
    max_chunk_lines: int = int(os.getenv("MAX_CHUNK_LINES", "60"))
    max_chunk_chars: int = int(os.getenv("MAX_CHUNK_CHARS", "2000"))
    overlap_lines: int = int(os.getenv("OVERLAP_LINES", "10"))
    top_k: int = int(os.getenv("TOP_K", "15"))
    rerank_candidates: int = int(os.getenv("RERANK_CANDIDATES", "50"))
    reranker_url: str = os.getenv("RERANKER_URL", "http://reranker:80")
    reranker_model: str = os.getenv("RERANKER_MODEL", "onnx-community/bge-reranker-v2-m3-ONNX")
    rerank_enabled: bool = os.getenv("RERANK_ENABLED", "true").lower() == "true"
    rerank_timeout: float = float(os.getenv("RERANK_TIMEOUT", "60"))
    rerank_text_chars: int = int(os.getenv("RERANK_TEXT_CHARS", "256"))
    rerank_min_score: float = float(os.getenv("RERANK_MIN_SCORE", "0.05"))


cfg = Config()
