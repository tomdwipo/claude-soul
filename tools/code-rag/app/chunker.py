import hashlib
import re
from dataclasses import dataclass
from pathlib import Path

from .config import cfg

KT_DECL = re.compile(
    r"^\s*(?:@\w+\s*)*(?:public|private|internal|open|abstract|sealed|data|)?\s*"
    r"(fun|class|object|interface|enum class)\s+([A-Za-z0-9_]+)"
)
MD_HEAD = re.compile(r"^(#{1,6})\s+(.*)")


@dataclass
class Chunk:
    path: str
    lang: str
    start_line: int
    end_line: int
    symbol: str
    text: str

    @property
    def content_sha(self) -> str:
        return hashlib.sha256(self.text.encode("utf-8", "ignore")).hexdigest()


def _lang(p: str) -> str:
    if p.endswith((".kt", ".kts")):
        return "kotlin"
    if p.endswith(".md"):
        return "markdown"
    return "xml"


def chunk_file(abs_path: Path, rel_path: str) -> list[Chunk]:
    lines = abs_path.read_text("utf-8", "ignore").splitlines()
    lang = _lang(rel_path)
    decl = KT_DECL if lang == "kotlin" else MD_HEAD if lang == "markdown" else None
    chunks: list[Chunk] = []
    buf: list[str] = []
    start = 0
    symbol = ""

    def flush(end: int) -> None:
        if buf and any(l.strip() for l in buf):
            chunks.append(Chunk(rel_path, lang, start + 1, end, symbol or "(file)", "\n".join(buf)))

    for i, line in enumerate(lines):
        boundary = bool(decl and decl.match(line))
        too_many_lines = (i - start) >= cfg.max_chunk_lines
        too_many_chars = sum(len(l) for l in buf) >= cfg.max_chunk_chars
        if (boundary and buf) or too_many_lines or too_many_chars:
            flush(i)
            start = i if boundary else max(i - cfg.overlap_lines, 0)
            buf = lines[start:i]
        if boundary:
            symbol = line.strip()[:120]
        buf.append(line)

    flush(len(lines))
    return chunks
