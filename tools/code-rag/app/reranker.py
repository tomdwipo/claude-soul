import httpx

from .config import cfg


async def rerank(query: str, candidates: list, top_k: int) -> list:
    if not candidates:
        return []
    if not cfg.rerank_enabled:
        return candidates[:top_k]
    texts = [c.payload["text"][: cfg.rerank_text_chars] for c in candidates]
    try:
        async with httpx.AsyncClient(timeout=cfg.rerank_timeout) as client:
            r = await client.post(
                f"{cfg.reranker_url}/rerank",
                json={"query": query, "texts": texts, "raw_scores": False},
            )
            r.raise_for_status()
            ranked = r.json()
    except Exception as e:
        print(f"[rerank] fallback to hybrid order: {type(e).__name__} {e}", flush=True)
        return candidates[:top_k]
    return [candidates[item["index"]] for item in ranked[:top_k]]
