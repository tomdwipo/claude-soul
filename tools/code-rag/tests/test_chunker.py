from pathlib import Path

from app.chunker import chunk_file


def _write(tmp_path: Path, name: str, body: str) -> Path:
    p = tmp_path / name
    p.write_text(body, encoding="utf-8")
    return p


def test_kotlin_splits_on_declarations(tmp_path):
    body = "\n".join(
        ["package a"]
        + ["fun one() {", "  val x = 1", "}"]
        + ["fun two() {", "  val y = 2", "}"]
        + ["class Three {", "  val z = 3", "}"]
    )
    chunks = chunk_file(_write(tmp_path, "A.kt", body), "A.kt")
    assert len(chunks) >= 3
    symbols = [c.symbol for c in chunks]
    assert any(s.startswith("fun one") for s in symbols)
    assert any(s.startswith("class Three") for s in symbols)
    assert all(c.lang == "kotlin" for c in chunks)


def test_markdown_carries_heading_symbol(tmp_path):
    body = "\n".join(["# Title", "intro", "## Section A", "text a", "## Section B", "text b"])
    chunks = chunk_file(_write(tmp_path, "doc.md", body), "doc.md")
    symbols = " ".join(c.symbol for c in chunks)
    assert "Section A" in symbols or "Section B" in symbols
    assert all(c.lang == "markdown" for c in chunks)


def test_empty_file_yields_nothing(tmp_path):
    chunks = chunk_file(_write(tmp_path, "Empty.kt", "\n\n   \n"), "Empty.kt")
    assert chunks == []


def test_content_sha_stable_for_same_text(tmp_path):
    body = "fun a() {}\n"
    a = chunk_file(_write(tmp_path, "A.kt", body), "A.kt")
    b = chunk_file(_write(tmp_path, "A.kt", body), "A.kt")
    assert a[0].content_sha == b[0].content_sha
