from app import mcp_server


class _Hit:
    def __init__(self, path, start, end, lang, symbol, text):
        self.payload = {
            "path": path,
            "start_line": start,
            "end_line": end,
            "lang": lang,
            "symbol": symbol,
            "text": text,
        }


async def test_search_code_formats_hits(monkeypatch):
    async def fake_embed(texts, is_query):
        return [[0.1, 0.2]]

    def fake_hybrid(qvec, query, n):
        return [_Hit("feature-lending/Foo.kt", 10, 20, "kotlin", "fun foo", "fun foo() {}")]

    async def fake_rerank(query, candidates, top_k):
        return candidates[:top_k]

    monkeypatch.setattr(mcp_server, "embed", fake_embed)
    monkeypatch.setattr(mcp_server.store, "hybrid_search", fake_hybrid)
    monkeypatch.setattr(mcp_server, "rerank", fake_rerank)

    result = await mcp_server.search_code("transfer validation", 3)
    assert "feature-lending/Foo.kt:10-20" in result
    assert "```" in result


async def test_search_code_no_matches(monkeypatch):
    async def fake_embed(texts, is_query):
        return [[0.1]]

    monkeypatch.setattr(mcp_server, "embed", fake_embed)
    monkeypatch.setattr(mcp_server.store, "hybrid_search", lambda *a: [])

    async def fake_rerank(query, candidates, top_k):
        return []

    monkeypatch.setattr(mcp_server, "rerank", fake_rerank)
    result = await mcp_server.search_code("nothing", 3)
    assert "No matches" in result
