from mcp.server.fastmcp import FastMCP

from . import qdrant_store as store
from .config import cfg
from .embedder import embed
from .reranker import rerank

mcp = FastMCP("code-rag", host="0.0.0.0", port=8080)  # nosec B104 - localhost-only dev container; must bind all interfaces to be reachable from host


@mcp.tool()
async def search_code(query: str, top_k: int = 0, candidates: int = 0) -> str:
    """Semantic + keyword search over this repository (source code AND docs/markdown).
    Returns ranked snippets with path:line anchors. Natural-language query, any language.

    top_k: number of final results (default 15).
    candidates: stage-1 recall pool re-scored by the reranker (default 50). Higher = better
    recall but slower rerank; lower it for faster queries."""
    k = top_k or cfg.top_k
    n = candidates or cfg.rerank_candidates
    qvec = (await embed([query], is_query=True))[0]
    pool = store.hybrid_search(qvec, query, n)
    hits = await rerank(query, pool, k)
    if not hits:
        return "No matches. Try broader terms or a symbol name."
    out = []
    for h in hits:
        p = h.payload
        out.append(
            f"### {p['path']}:{p['start_line']}-{p['end_line']}  ({p['lang']})\n"
            f"symbol: {p['symbol']}\n```\n{p['text']}\n```"
        )
    return "\n\n".join(out)


if __name__ == "__main__":
    store.ensure_collection()
    mcp.run(transport="streamable-http")
