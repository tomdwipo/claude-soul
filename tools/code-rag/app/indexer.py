import asyncio
import sys
from pathlib import Path

from . import qdrant_store as store
from .chunker import chunk_file
from .config import cfg
from .embedder import embed


def iter_files():
    root = Path(cfg.repo_root)
    for p in root.rglob("*"):
        if p.suffix in cfg.include_ext and not any(d in p.parts for d in cfg.exclude_dirs):
            yield p, str(p.relative_to(root))


async def _index_one(abs_p: Path, rel: str) -> int:
    if not abs_p.exists():
        store.delete_by_paths([rel])
        print(f"[index] PRUNE {rel}: file gone", flush=True)
        return 0
    chunks = chunk_file(abs_p, rel)
    known = store.existing_shas([rel])
    current_ids = {store.point_id(c.path, c.start_line) for c in chunks}
    stale = [pid for pid in known if pid not in current_ids]
    store.delete_points(stale)
    fresh = [
        c for c in chunks
        if known.get(store.point_id(c.path, c.start_line)) != c.content_sha
    ]
    if fresh:
        try:
            vecs = await embed([c.text for c in fresh], is_query=False)
            store.upsert(fresh, vecs)
        except Exception as e:
            print(f"[index] SKIP {rel}: {type(e).__name__} {e}", flush=True)
            return 0
    if fresh or stale:
        print(f"[index] {rel}: +{len(fresh)} chunks, -{len(stale)} stale", flush=True)
    return len(fresh)


async def index_paths(rel_paths: list[str] | None = None) -> int:
    store.ensure_collection()
    root = Path(cfg.repo_root)
    targets = [(root / r, r) for r in rel_paths] if rel_paths else list(iter_files())
    total = 0
    for abs_p, rel in targets:
        total += await _index_one(abs_p, rel)
    if rel_paths is None:
        current_paths = {rel for _, rel in targets}
        gone = list(store.all_indexed_paths() - current_paths)
        if gone:
            store.delete_by_paths(gone)
            print(f"[index] SWEEP: pruned {len(gone)} deleted files", flush=True)
    print(f"[index] done, {total} chunks upserted", flush=True)
    return total


if __name__ == "__main__":
    asyncio.run(index_paths(sys.argv[1:] or None))
