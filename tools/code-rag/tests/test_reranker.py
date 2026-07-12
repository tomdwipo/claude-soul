from app import reranker


class _Cand:
    def __init__(self, text):
        self.payload = {"text": text}


class _FakeResponse:
    def __init__(self, data):
        self._data = data

    def raise_for_status(self):
        return None

    def json(self):
        return self._data


class _FakeClient:
    def __init__(self, data):
        self._data = data

    async def __aenter__(self):
        return self

    async def __aexit__(self, *exc):
        return False

    async def post(self, url, json):
        return _FakeResponse(self._data)


def _patch(monkeypatch, data):
    monkeypatch.setattr(
        reranker.httpx, "AsyncClient", lambda *a, **k: _FakeClient(data)
    )


async def test_rerank_reorders_and_truncates(monkeypatch):
    cands = [_Cand("a"), _Cand("b"), _Cand("c")]
    _patch(monkeypatch, [{"index": 2, "score": 0.9}, {"index": 0, "score": 0.4}])
    out = await reranker.rerank("q", cands, top_k=2)
    assert [c.payload["text"] for c in out] == ["c", "a"]


async def test_rerank_empty_candidates(monkeypatch):
    out = await reranker.rerank("q", [], top_k=5)
    assert out == []


async def test_rerank_min_score_drops_low(monkeypatch):
    monkeypatch.setattr(reranker.cfg, "rerank_min_score", 0.05)
    cands = [_Cand("a"), _Cand("b"), _Cand("c")]
    _patch(monkeypatch, [{"index": 2, "score": 0.9}, {"index": 0, "score": 0.01}])
    out = await reranker.rerank("q", cands, top_k=5)
    assert [c.payload["text"] for c in out] == ["c"]
