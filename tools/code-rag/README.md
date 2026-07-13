# code-rag — local semantic code search as an MCP tool

Drop-in **developer tooling** that gives an AI agent (Claude Code, etc.) semantic + keyword search
over *your* repository — source code **and** docs — exposed as an MCP tool `search_code`. Runs fully
local (no code leaves your machine). Natural-language queries, any human language.

- **Embedding:** `qwen3-embedding:0.6b` on host **Ollama** (GPU/Metal accelerated — not in Docker).
- **Vector DB:** Qdrant (Docker, persisted volume).
- **Retrieval:** hybrid dense + BM25 (RRF) → `bge-reranker-v2-m3` int8 cross-encoder (ONNX). These two
  models make results **precise**: the embedder+reranker rank genuinely relevant code/docs first, and
  `RERANK_MIN_SCORE` (default 0.05) drops low-relevance hits — an off-topic query returns nothing
  instead of noise. Calibrate the cutoff per model (probe good vs garbage query; put it in the gap).
- **Auto-index + prune:** a watcher re-embeds only changed chunks and prunes stale/deleted ones, so
  the index tracks the working tree (edits, branch switches) with no manual rebuild.

Not shipped in your app — it's an out-of-band dev index that reads the working tree read-only.

## Why these models

| Role | Model | Why it's the default |
|------|-------|----------------------|
| **Embedding** | `qwen3-embedding:0.6b` | Strong **general** model (not code-only): its Qwen3 base is trained heavily on code (MTEB-Code ~75) **and** it's good on prose + **multilingual**. A code repo is really *code + docs*, and queries can be in any language — a code-only / English-only embedder would lose on the docs half and non-English queries. Small (~0.6B), Apache-2.0, runs on host Ollama (GPU/Metal). |
| **Reranker** | `bge-reranker-v2-m3` (int8) | Strong **general multilingual** cross-encoder — reads query+chunk jointly for precise ordering, works well on code+docs, handles non-English queries, Apache-2.0. No strong code-specialized reranker that's also multilingual + permissive. int8 ONNX keeps it CPU-viable. |

**Trade-off (honest):** both are deliberately *general*, not code-specialized. If your work is
**pure code, English-only**, a code-specialized embedder (e.g. `nomic-embed-code`, `CodeRankEmbed`)
could edge these on code-only retrieval — but at a cost (bigger, or English/Chinese-only, or a
non-commercial license). For a mixed code+docs repo with multilingual queries, the general pair is
the better fit. Swap via `EMBED_MODEL` / `RERANKER_MODEL` if your case differs.

## Prerequisites

- Docker (Desktop) with **≥ 8 GB** memory (the reranker needs headroom).
- [Ollama](https://ollama.com) running on the host (Apple Silicon → Metal; NVIDIA → CUDA).

## Security

The watcher/mcp-server mount your repo `:ro` and read the **filesystem** — `.gitignore` keeps a
secret out of a *commit*, it does nothing by itself against a local tool walking the working tree.
`RESPECT_GITIGNORE` (default `true`) closes that gap: both the watcher and the full-index pass ask
`git ls-files --others --ignored --exclude-standard` (delegated to git itself, not a hand-rolled
parser, so nested `.gitignore`, global excludes, and `.git/info/exclude` are all honored) and skip
anything git would ignore — `.mcp.json`, `service-account.json`, `.env`, whatever your `.gitignore`
already lists, all excluded automatically with zero per-project configuration. Fails open (indexes
normally) if `REPO_ROOT` isn't a git repo, so it never blocks a non-git checkout.

Belt-and-suspenders: `EXCLUDE_FILES` still applies on top (default includes `.mcp.json` even with
`RESPECT_GITIGNORE=false`), and a file that's `git add`-ed *before* a `.gitignore` rule existed
stays visible (git doesn't retroactively hide tracked files — same as `git status`). If a secret
was already indexed before this existed, purge it: `curl -X DELETE
http://localhost:6333/collections/<name>` (collections are isolated per project — this only
touches that one), then reindex.

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

**Adding several projects at once?** Their empty-collection first-indexes hit the single-slot
Ollama embed + shared Qdrant concurrently. The watcher is hardened for this — Qdrant calls
retry on timeout instead of crash-looping the container, and embed calls back off + retry
instead of dropping a file on the first `400`. Spread the cold-start herd with
`STARTUP_JITTER_SEC=8 make up-project …`. Note: `OLLAMA_NUM_PARALLEL` does **not** widen an
embedding runner (Ollama pins it to one slot) — concurrency comes from the client-side retry,
not the server knob.

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

`INCLUDE_EXT` / `EXCLUDE_DIRS` / `EXCLUDE_FILES` and `HF_TOKEN` / `COLLECTION` /
`STARTUP_JITTER_SEC` are forwarded into the containers by both compose files (`${VAR:-default}` in
their `environment:` blocks) — set them in `.env` or your shell and `make up`/`make up-project`
picks them up. The rest below (`TOP_K`, `RERANK_*`, `ORT_THREADS`, `EMBED_MODEL`, resilience knobs)
are read by `app/config.py` but **not yet wired through either compose file** — override them by
editing the `environment:` list directly if you need to change one.

`INCLUDE_EXT` / `EXCLUDE_DIRS` / `EXCLUDE_FILES` (comma-separated — tune for your stack;
`EXCLUDE_FILES` drops generated noise by basename: lockfiles + `lint-baseline.xml` by default,
so a generated suppression list / lockfile never pollutes search), `TOP_K` (default 15),
`RERANK_CANDIDATES` (50), `RERANK_TEXT_CHARS` (256), `RERANK_MIN_SCORE` (0.05), `RERANK_TIMEOUT` (60), `RERANK_ENABLED`,
`ORT_THREADS`, `EMBED_MODEL`, `COLLECTION`, `HF_TOKEN` (optional, faster model downloads).
Resilience/scaling: `QDRANT_TIMEOUT` (30), `QDRANT_MAX_RETRIES` (3), `EMBED_MAX_RETRIES` (4),
`EMBED_RETRY_BASE` (0.75 s), `EMBED_BATCH_CHARS` (6000 — sub-batch embed input so a big
many-chunk file can't overflow the server batch), `STARTUP_JITTER_SEC` (0 — set when starting
many projects at once).
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
