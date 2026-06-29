Intelligent search for: $ARGUMENTS

Execute multi-tier search strategy:

**Tier 1 - Vector Search:**
- Target: Qdrant collection `ws-99ba28f992cd224e`
- Engine: Ollama
- Config: 50 results max, 0.55 similarity threshold

**Tier 2 - Codebase Search:**
- Activate if: Qdrant MCP unavailable OR results < threshold
- Method: Pattern matching + content analysis
- Scope: Project files relevant to query

**Deliverable:**
Ranked list of relevant files with:
- Relevance explanation
- Key sections/functions
- Confidence scores (if available)