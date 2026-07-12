import uuid

from fastembed import SparseTextEmbedding
from qdrant_client import QdrantClient, models

from .config import cfg

_client: QdrantClient | None = None
_bm25: SparseTextEmbedding | None = None


def _qdrant() -> QdrantClient:
    global _client
    if _client is None:
        _client = QdrantClient(url=cfg.qdrant_url)
    return _client


def _sparse() -> SparseTextEmbedding:
    global _bm25
    if _bm25 is None:
        _bm25 = SparseTextEmbedding("Qdrant/bm25")
    return _bm25


def ensure_collection() -> None:
    client = _qdrant()
    if client.collection_exists(cfg.collection):
        return
    client.create_collection(
        cfg.collection,
        vectors_config={
            "dense": models.VectorParams(size=cfg.dense_dim, distance=models.Distance.COSINE)
        },
        sparse_vectors_config={"bm25": models.SparseVectorParams()},
    )


def point_id(path: str, start: int) -> str:
    return str(uuid.uuid5(uuid.NAMESPACE_URL, f"{path}#{start}"))


def upsert(chunks, dense_vecs) -> None:
    sparse = list(_sparse().embed([c.text for c in chunks]))
    points = [
        models.PointStruct(
            id=point_id(c.path, c.start_line),
            vector={
                "dense": d,
                "bm25": models.SparseVector(indices=s.indices.tolist(), values=s.values.tolist()),
            },
            payload={
                "path": c.path,
                "lang": c.lang,
                "start_line": c.start_line,
                "end_line": c.end_line,
                "symbol": c.symbol,
                "text": c.text,
                "content_sha": c.content_sha,
            },
        )
        for c, d, s in zip(chunks, dense_vecs, sparse)
    ]
    _qdrant().upsert(cfg.collection, points)


def existing_shas(paths: list[str]) -> dict[str, str]:
    res, _ = _qdrant().scroll(
        cfg.collection,
        with_payload=["content_sha", "path"],
        scroll_filter=models.Filter(
            must=[models.FieldCondition(key="path", match=models.MatchAny(any=paths))]
        ),
        limit=10000,
    )
    return {p.id: p.payload["content_sha"] for p in res}


def delete_points(ids: list[str]) -> None:
    if not ids:
        return
    _qdrant().delete(cfg.collection, points_selector=models.PointIdsList(points=ids))


def delete_by_paths(paths: list[str]) -> None:
    if not paths:
        return
    _qdrant().delete(
        cfg.collection,
        points_selector=models.FilterSelector(
            filter=models.Filter(
                must=[models.FieldCondition(key="path", match=models.MatchAny(any=paths))]
            )
        ),
    )


def all_indexed_paths() -> set[str]:
    paths: set[str] = set()
    offset = None
    while True:
        res, offset = _qdrant().scroll(
            cfg.collection, with_payload=["path"], with_vectors=False, limit=1000, offset=offset
        )
        for p in res:
            paths.add(p.payload["path"])
        if offset is None:
            break
    return paths


def hybrid_search(query_dense, query_text: str, n_candidates: int):
    sparse = next(_sparse().embed([query_text]))
    return _qdrant().query_points(
        cfg.collection,
        prefetch=[
            models.Prefetch(query=query_dense, using="dense", limit=n_candidates * 2),
            models.Prefetch(
                query=models.SparseVector(indices=sparse.indices.tolist(), values=sparse.values.tolist()),
                using="bm25",
                limit=n_candidates * 2,
            ),
        ],
        query=models.FusionQuery(fusion=models.Fusion.RRF),
        limit=n_candidates,
        with_payload=True,
    ).points
