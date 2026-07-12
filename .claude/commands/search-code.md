# /search-code — semantic code + docs search (code-rag MCP)

Semantic + keyword search over this repository (source code **and** docs) via the local **code-rag**
MCP tool (see `tools/code-rag/`). Natural-language query, any language.

Usage:
```
/search-code <query>
/search-code <query> | fast          # candidates=20 (~8s), quick lookup
/search-code <query> | deep          # candidates=80, top_k=25 (max recall, slower)
/search-code <query> | top_k=N candidates=M
```

## What to do

1. Parse `$ARGUMENTS`: text before `|` is the **query**; after `|` are options
   (`fast`, `deep`, or explicit `top_k=N` / `candidates=M`).
1b. **Pick the server.** If several `code-rag-<folder>` MCP servers exist (parallel checkouts), call
   the one whose `<folder>` matches the basename of the current repo root. If only a bare `code-rag`
   exists (single-stack), use that.
2. Call the **`search_code`** MCP tool with `query`, and `top_k`/`candidates` only if the user gave
   options (defaults: `candidates=50`, `top_k=15`; `fast`→20; `deep`→80/25). If its schema is
   deferred, load it first (`ToolSearch "select:mcp__code-rag*__search_code"`).
3. Present ranked hits as `path:start-end` (clickable) + enclosing symbol + a 1-line why-it-matches;
   lead with the most relevant, summarize rather than dumping raw chunks. Read the top hits for depth.

## If the tool errors / isn't connected

The local stack isn't running. Fall back to Grep/Glob, and tell the user: `cd tools/code-rag &&
make up`, then restart the agent so the `code-rag` MCP server connects. Full docs: `tools/code-rag/README.md`.
