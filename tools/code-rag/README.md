# code-rag — local semantic code search as an MCP tool

Drop-in **developer tooling** that gives an AI agent (Claude Code, etc.) semantic + keyword search
over *your* repository — source code **and** docs — exposed as an MCP tool `search_code`. Runs fully
local (no code leaves your machine). Natural-language queries, any human language.

- **Embedding:** `qwen3-embedding:0.6b` on host **Ollama** (GPU/Metal accelerated — not in Docker).
- **Vector DB:** Qdrant (Docker, persisted volume).
- **Retrieval:** hybrid dense + BM25 (RRF) → `bge-reranker-v2-m3` int8 cross-encoder (ONNX).
- **Auto-index + prune:** a watcher re-embeds only changed chunks and prunes stale/deleted ones, so
  the index tracks the working tree (edits, branch switches) with no manual rebuild.

Not shipped in your app — it's an out-of-band dev index that reads the working tree read-only.

## Prerequisites

- Docker (Desktop) with **≥ 8 GB** memory (the reranker needs headroom).
- [Ollama](https://ollama.com) running on the host (Apple Silicon → Metal; NVIDIA → CUDA).

## Quickstart (single repo)

```bash
cd tools/code-rag
make up          # pulls qwen3-embedding, builds + starts qdrant + reranker + mcp-server + watcher
```

Register the tool in your agent's MCP config (e.g. `.mcp.json`):

```json
"code-rag": { "type": "http", "url": "http://localhost:8080/mcp" }
```

The index builds on first boot in a few minutes; it's **local per machine** and rebuilds
incrementally as files change.

## Multiple checkouts in parallel

Several checkouts of the same repo (different branches) at once? A single index would mix them.
Use **shared heavy infra + a light per-checkout stack** — one Qdrant + one reranker shared, a
`watcher`+`mcp-server` per checkout with its own collection + port (fits ~2.3 GB total):

```bash
cd tools/code-rag                        # run from the one checkout that has this folder
make up-shared                           # qdrant + reranker (once)
make up-project MCP_PORT=8080            # this checkout   → collection = folder name
make up-project REPO_ROOT=/abs/checkout-b MCP_PORT=8081
make up-project REPO_ROOT=/abs/checkout-c MCP_PORT=8082
```

Each `up-project` prints the `.mcp.json` entry to add (`code-rag-<folder>` → its port). **Collection =
directory basename** (stable when the folder's branch changes). Single-stack (`make up`) and
multi-project both bind Qdrant on 6333 — run one mode at a time.

## Make targets

| Target | Effect |
|--------|--------|
| `make up` / `make down` | single-stack up / down |
| `make reindex` | force a full re-index |
| `make logs` | tail the watcher |
| `make test` | `uv run pytest` (unit tests, no network) |
| `make up-shared` / `make down-shared` | shared qdrant + reranker (multi-project) |
| `make up-project MCP_PORT=N [REPO_ROOT=/path]` | per-checkout watcher + mcp-server |
| `make down-project [REPO_ROOT=/path]` / `make logs-project` | stop / tail a per-checkout stack |

## Configuration (env / `.env`)

`INCLUDE_EXT` / `EXCLUDE_DIRS` (comma-separated — tune for your stack), `TOP_K` (default 15),
`RERANK_CANDIDATES` (50), `RERANK_TEXT_CHARS` (256), `RERANK_TIMEOUT` (60), `RERANK_ENABLED`,
`ORT_THREADS`, `EMBED_MODEL`, `COLLECTION`, `HF_TOKEN` (optional, faster model downloads).
`search_code(query, top_k, candidates)` — the caller can override per query.

## How it works

```
Agent ──MCP :8080──▶ mcp-server ──embed──▶ Ollama (host, GPU/Metal)
                          │ hybrid query (dense + BM25, RRF)
                          ▼
                       Qdrant ──candidates──▶ reranker (int8 ONNX cross-encoder)
                          ▲ upsert/prune
                       watcher (mounts repo :ro, watchdog + content_sha incremental + prune)
```

## Notes

- **Host acceleration matters.** Docker Desktop on macOS has no GPU passthrough, so the embedding
  model runs on the **host** via Ollama; Docker holds only the vector DB + reranker + watcher.
- **Reranker = prebuilt int8 ONNX** (`onnx-community/bge-reranker-v2-m3-ONNX`) served by a small
  Python service — no local export/quantize. Cached in a volume (instant on 2nd boot).
- **Latency** is CPU-bound (~19–22 s @ 50 candidates, ~8 s @ 20 on an M-series CPU). Lower
  `candidates` per query for speed — it's the recall/latency knob.
- **Containers run as non-root**; search falls back to hybrid (RRF) order if the reranker times out.
- Both modes auto-start on Docker launch (`restart: unless-stopped`) — as long as **Ollama** is running.
