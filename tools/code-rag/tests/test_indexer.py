from app import indexer
from app import qdrant_store as store


class FakeStore:
    def __init__(self):
        self.points: dict[str, tuple[str, str]] = {}

    def ensure_collection(self):
        pass

    def existing_shas(self, paths):
        ps = set(paths)
        return {i: v[1] for i, v in self.points.items() if v[0] in ps}

    def upsert(self, chunks, _vecs):
        for c in chunks:
            self.points[store.point_id(c.path, c.start_line)] = (c.path, c.content_sha)

    def delete_points(self, ids):
        for i in ids:
            self.points.pop(i, None)

    def delete_by_paths(self, paths):
        ps = set(paths)
        for i in [i for i, v in self.points.items() if v[0] in ps]:
            self.points.pop(i, None)

    def all_indexed_paths(self):
        return {v[0] for v in self.points.values()}


def _wire(monkeypatch, tmp_path, fake, embedded):
    monkeypatch.setattr(indexer.cfg, "repo_root", str(tmp_path))
    monkeypatch.setattr(store, "ensure_collection", fake.ensure_collection)
    monkeypatch.setattr(store, "existing_shas", fake.existing_shas)
    monkeypatch.setattr(store, "upsert", fake.upsert)
    monkeypatch.setattr(store, "delete_points", fake.delete_points)
    monkeypatch.setattr(store, "delete_by_paths", fake.delete_by_paths)
    monkeypatch.setattr(store, "all_indexed_paths", fake.all_indexed_paths)

    async def fake_embed(texts, is_query, skip_failed=False):
        embedded.extend(texts)
        return [[0.0] for _ in texts]

    monkeypatch.setattr(indexer, "embed", fake_embed)


async def test_incremental_reembeds_only_changed(tmp_path, monkeypatch):
    fake, embedded = FakeStore(), []
    _wire(monkeypatch, tmp_path, fake, embedded)
    (tmp_path / "A.kt").write_text("fun a() {}\n", encoding="utf-8")
    (tmp_path / "B.kt").write_text("fun b() {}\n", encoding="utf-8")

    assert await indexer.index_paths() == 2
    assert len(embedded) == 2

    embedded.clear()
    (tmp_path / "B.kt").write_text("fun b() {\n  val changed = 1\n}\n", encoding="utf-8")
    assert await indexer.index_paths() == 1
    assert len(embedded) == 1


async def test_prune_stale_on_shrink(tmp_path, monkeypatch):
    fake, embedded = FakeStore(), []
    _wire(monkeypatch, tmp_path, fake, embedded)
    (tmp_path / "A.kt").write_text("fun a() {}\nfun b() {}\nfun c() {}\n", encoding="utf-8")
    await indexer.index_paths()
    assert len([i for i, v in fake.points.items() if v[0] == "A.kt"]) >= 3

    (tmp_path / "A.kt").write_text("fun only() {}\n", encoding="utf-8")
    await indexer.index_paths(["A.kt"])
    a_ids = {i for i, v in fake.points.items() if v[0] == "A.kt"}
    assert a_ids == {store.point_id("A.kt", 1)}


async def test_deleted_file_pruned(tmp_path, monkeypatch):
    fake, embedded = FakeStore(), []
    _wire(monkeypatch, tmp_path, fake, embedded)
    (tmp_path / "A.kt").write_text("fun a() {}\n", encoding="utf-8")
    (tmp_path / "B.kt").write_text("fun b() {}\n", encoding="utf-8")
    await indexer.index_paths()

    (tmp_path / "B.kt").unlink()
    await indexer.index_paths(["B.kt"])
    assert not any(v[0] == "B.kt" for v in fake.points.values())
    assert any(v[0] == "A.kt" for v in fake.points.values())


async def test_full_run_sweep_removes_gone_files(tmp_path, monkeypatch):
    fake, embedded = FakeStore(), []
    _wire(monkeypatch, tmp_path, fake, embedded)
    (tmp_path / "A.kt").write_text("fun a() {}\n", encoding="utf-8")
    (tmp_path / "B.kt").write_text("fun b() {}\n", encoding="utf-8")
    await indexer.index_paths()

    (tmp_path / "B.kt").unlink()
    await indexer.index_paths()
    assert fake.all_indexed_paths() == {"A.kt"}
