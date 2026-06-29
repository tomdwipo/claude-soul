# Advanced Search Command

Search and analyze: $ARGUMENTS

## Search Strategy (in order of priority):

### 1. Vector Database Search
- **Database**: Qdrant vector collection `ws-99ba28f992cd224e`
- **Model**: Ollama
- **Parameters**:
    - Limit: 50 results
    - Similarity threshold: 0.55

### 2. Fallback to Codebase Search
If Qdrant MCP server is unavailable or returns insufficient results:
- Search local codebase for relevant files
- Use pattern matching and content analysis
- Focus on files related to the query context

## Execution Steps:
1. **Parse Query**: Understand what the user is asking for
2. **Vector Search**: Query Qdrant database using semantic similarity
3. **Validate Results**: Check if results meet relevance threshold
4. **Fallback Search**: If needed, search local files using grep/ripgrep
5. **Compile Results**: Present the most relevant files and their context

## Output Format:
- List relevant files found
- Include brief description of why each file is relevant
- Show confidence/similarity scores where available
- Highlight key sections or functions within files
