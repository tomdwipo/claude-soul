REPO_ROOT ?= $(shell cd ../.. && pwd)
export REPO_ROOT

# ── single-stack (one repo, the simple case) ──
up:
	ollama pull qwen3-embedding:0.6b && docker compose up -d --build

down:
	docker compose down

reindex:
	docker compose exec watcher uv run python -m app.indexer

logs:
	docker compose logs -f watcher

test:
	uv run pytest

# ── multi-project (parallel checkouts): shared Qdrant+reranker + per-checkout watcher/mcp ──
# 1) once:      make up-shared
# 2) per repo:  make up-project MCP_PORT=8080                 (current checkout)
#               make up-project REPO_ROOT=/path/to/other MCP_PORT=8081
#    COLLECTION is auto-derived from the checkout's folder name.
up-shared:
	ollama pull qwen3-embedding:0.6b && docker compose -f docker-compose.shared.yml up -d --build

down-shared:
	docker compose -f docker-compose.shared.yml down

up-project:
	@test -n "$(MCP_PORT)" || { echo "usage: make up-project [REPO_ROOT=/path] MCP_PORT=8080"; exit 1; }
	REPO_ROOT="$(abspath $(REPO_ROOT))" \
	COLLECTION="$(notdir $(abspath $(REPO_ROOT)))" \
	MCP_PORT="$(MCP_PORT)" \
	COMPOSE_PROJECT_NAME="code-rag-$(notdir $(abspath $(REPO_ROOT)))" \
	docker compose -f docker-compose.project.yml up -d --build
	@echo 'MCP entry (add to .mcp.json): "code-rag-$(notdir $(abspath $(REPO_ROOT)))": { "type": "http", "url": "http://localhost:$(MCP_PORT)/mcp" }'

down-project:
	COMPOSE_PROJECT_NAME="code-rag-$(notdir $(abspath $(REPO_ROOT)))" \
	docker compose -f docker-compose.project.yml down

logs-project:
	COMPOSE_PROJECT_NAME="code-rag-$(notdir $(abspath $(REPO_ROOT)))" \
	docker compose -f docker-compose.project.yml logs -f watcher
