import asyncio

import httpx

from .config import cfg

_INSTRUCT = "Instruct: Retrieve code and documentation relevant to the query\nQuery: "
_MAX_CHARS = 4000


def _prepare(text: str, is_query: bool) -> str:
    t = text if text.strip() else " "
    if len(t) > _MAX_CHARS:
        t = t[:_MAX_CHARS]
    return (_INSTRUCT + t) if is_query else t


def _batches(payload_input: list[str]) -> list[list[str]]:
    out: list[list[str]] = []
    cur: list[str] = []
    cur_len = 0
    for item in payload_input:
        if cur and cur_len + len(item) > cfg.embed_batch_chars:
            out.append(cur)
            cur, cur_len = [], 0
        cur.append(item)
        cur_len += len(item)
    if cur:
        out.append(cur)
    return out


async def _embed_batch(payload_input: list[str]) -> list[list[float]]:
    last: Exception | None = None
    for attempt in range(1, cfg.embed_max_retries + 1):
        try:
            async with httpx.AsyncClient(timeout=120) as client:
                r = await client.post(
                    f"{cfg.ollama_url}/api/embed",
                    json={"model": cfg.embed_model, "input": payload_input},
                )
                r.raise_for_status()
                return r.json()["embeddings"]
        except (httpx.HTTPStatusError, httpx.TransportError) as e:
            last = e
            if attempt < cfg.embed_max_retries:
                delay = cfg.embed_retry_base * (2 ** (attempt - 1))
                print(f"[embed] retry {attempt}/{cfg.embed_max_retries} after {delay:.1f}s: {e}", flush=True)
                await asyncio.sleep(delay)
    raise last


async def embed(
    texts: list[str], is_query: bool, skip_failed: bool = False
) -> list[list[float] | None]:
    payload_input = [_prepare(t, is_query) for t in texts]
    out: list[list[float] | None] = []
    for batch in _batches(payload_input):
        try:
            out.extend(await _embed_batch(batch))
        except (httpx.HTTPStatusError, httpx.TransportError) as e:
            if not skip_failed:
                raise
            print(f"[embed] sub-batch failed, dropping {len(batch)} chunks (retry next pass): {e}", flush=True)
            out.extend([None] * len(batch))
    return out
