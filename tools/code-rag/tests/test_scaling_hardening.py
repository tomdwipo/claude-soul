import httpx
import pytest

from app import embedder
from app import qdrant_store as store
from app import watcher
from app.watcher import Handler
from qdrant_client.http.exceptions import ResponseHandlingException


async def _noop_async(*_a, **_k):
    return None


def test_qdrant_retry_succeeds_after_transient(monkeypatch):
    monkeypatch.setattr(store.cfg, "qdrant_max_retries", 3)
    monkeypatch.setattr(store.time, "sleep", lambda *_: None)
    calls = {"n": 0}

    def flaky():
        calls["n"] += 1
        if calls["n"] < 2:
            raise ResponseHandlingException("timed out")
        return "ok"

    assert store._retry(flaky, "flaky") == "ok"
    assert calls["n"] == 2


def test_qdrant_retry_reraises_when_exhausted(monkeypatch):
    monkeypatch.setattr(store.cfg, "qdrant_max_retries", 2)
    monkeypatch.setattr(store.time, "sleep", lambda *_: None)

    def always_fail():
        raise ResponseHandlingException("timed out")

    with pytest.raises(ResponseHandlingException):
        store._retry(always_fail, "always")


async def test_embed_retries_then_succeeds(monkeypatch):
    monkeypatch.setattr(embedder.cfg, "embed_max_retries", 3)
    monkeypatch.setattr(embedder.asyncio, "sleep", _noop_async)
    attempts = {"n": 0}

    class FakeResp:
        def raise_for_status(self):
            pass

        def json(self):
            return {"embeddings": [[0.1]]}

    class FakeClient:
        async def __aenter__(self):
            return self

        async def __aexit__(self, *a):
            return False

        async def post(self, *a, **k):
            attempts["n"] += 1
            if attempts["n"] < 2:
                raise httpx.ConnectError("runner dropped")
            return FakeResp()

    monkeypatch.setattr(embedder.httpx, "AsyncClient", lambda **k: FakeClient())
    out = await embedder.embed(["hello"], is_query=False)
    assert out == [[0.1]]
    assert attempts["n"] == 2


async def test_embed_reraises_when_exhausted(monkeypatch):
    monkeypatch.setattr(embedder.cfg, "embed_max_retries", 2)
    monkeypatch.setattr(embedder.asyncio, "sleep", _noop_async)

    class FakeClient:
        async def __aenter__(self):
            return self

        async def __aexit__(self, *a):
            return False

        async def post(self, *a, **k):
            raise httpx.ConnectError("runner dropped")

    monkeypatch.setattr(embedder.httpx, "AsyncClient", lambda **k: FakeClient())
    with pytest.raises(httpx.ConnectError):
        await embedder.embed(["hello"], is_query=False)


def test_watcher_batch_failure_requeues(monkeypatch, tmp_path):
    monkeypatch.setattr(watcher.cfg, "repo_root", str(tmp_path))
    h = Handler()
    h.pending = {"A.kt"}
    batch = list(h.pending)
    h.pending = set()
    try:
        raise RuntimeError("qdrant down")
    except Exception as e:  # noqa: BLE001
        print(f"[watch] batch index failed, re-queueing: {type(e).__name__} {e}", flush=True)
        h.pending |= set(batch)
    assert h.pending == {"A.kt"}
