import types

import httpx
import pytest

from app import embedder
from app import indexer
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


def test_embed_splits_into_char_bounded_batches(monkeypatch):
    monkeypatch.setattr(embedder.cfg, "embed_batch_chars", 6000)
    items = ["x" * 4000, "y" * 4000, "z" * 1000]
    batches = embedder._batches(items)
    assert [len(b) for b in batches] == [1, 2]
    assert sum(len(b) for b in batches) == len(items)


async def test_embed_subbatches_across_multiple_posts(monkeypatch):
    monkeypatch.setattr(embedder.cfg, "embed_batch_chars", 6000)
    monkeypatch.setattr(embedder.cfg, "embed_max_retries", 2)
    posted = []

    class FakeResp:
        def __init__(self, n):
            self._n = n

        def raise_for_status(self):
            pass

        def json(self):
            return {"embeddings": [[0.1]] * self._n}

    class FakeClient:
        async def __aenter__(self):
            return self

        async def __aexit__(self, *a):
            return False

        async def post(self, *a, **k):
            n = len(k["json"]["input"])
            posted.append(n)
            return FakeResp(n)

    monkeypatch.setattr(embedder.httpx, "AsyncClient", lambda **k: FakeClient())
    out = await embedder.embed(["a" * 4000, "b" * 4000, "c" * 1000], is_query=False)
    assert len(out) == 3
    assert posted == [1, 2]


async def test_embed_skip_failed_drops_only_failed_batch(monkeypatch):
    monkeypatch.setattr(embedder.cfg, "embed_batch_chars", 6000)
    monkeypatch.setattr(embedder.cfg, "embed_max_retries", 1)
    monkeypatch.setattr(embedder.asyncio, "sleep", _noop_async)
    calls = {"n": 0}

    class FakeResp:
        def raise_for_status(self):
            pass

        def json(self):
            return {"embeddings": [[0.2]]}

    class FakeClient:
        async def __aenter__(self):
            return self

        async def __aexit__(self, *a):
            return False

        async def post(self, *a, **k):
            calls["n"] += 1
            if calls["n"] == 1:
                raise httpx.ConnectError("boom")
            return FakeResp()

    monkeypatch.setattr(embedder.httpx, "AsyncClient", lambda **k: FakeClient())
    out = await embedder.embed(["a" * 4000, "b" * 4000], is_query=False, skip_failed=True)
    assert out[0] is None
    assert out[1] == [0.2]


def test_iter_files_excludes_baseline(monkeypatch, tmp_path):
    monkeypatch.setattr(indexer.cfg, "repo_root", str(tmp_path))
    monkeypatch.setattr(indexer.cfg, "exclude_files", ("lint-baseline.xml",))
    (tmp_path / "A.kt").write_text("fun a() {}", encoding="utf-8")
    (tmp_path / "lint-baseline.xml").write_text("<issues/>", encoding="utf-8")
    rels = {rel for _, rel in indexer.iter_files()}
    assert "A.kt" in rels
    assert "lint-baseline.xml" not in rels


def test_watcher_excludes_baseline_file(monkeypatch, tmp_path):
    monkeypatch.setattr(watcher.cfg, "repo_root", str(tmp_path))
    monkeypatch.setattr(watcher.cfg, "exclude_files", ("lint-baseline.xml",))
    h = Handler()
    h.on_any_event(
        types.SimpleNamespace(src_path=str(tmp_path / "core-ui" / "lint-baseline.xml"), is_directory=False)
    )
    assert h.pending == set()


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
