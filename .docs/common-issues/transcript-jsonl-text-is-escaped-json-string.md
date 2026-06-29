# Reading markers/text from a transcript JSONL: it's an escaped JSON string — parse the line, don't grep raw

**Symptom:** a Stop/PostToolUse hook reads the conversation transcript (`transcript_path`) to extract
something the assistant wrote — e.g. a `<!--CALIB {"claim":"…","confidence":"High"}-->` marker — by
grepping the raw file + `json.loads` on the captured group. It finds **0** matches even though the
marker is clearly in the transcript. (Evidence: `calib.py capture` first build → `captured 0` despite
2 valid markers in the file.)

**Cause:** the assistant's message text is stored **as a JSON string value** inside each JSONL line
(`{"message":{"content":[{"type":"text","text":"… <!--CALIB {\"claim\":\"…\"}--> …"}]}}`). So in the
**raw** file the marker's inner quotes arrive **escaped** (`\"`). A regex match on raw text yields
`{\"claim\":\"…\"}`, and `json.loads` on that backslash-laden string raises → silently skipped.

**Fix:** parse the JSONL **line by line** (`json.loads(line)`) — that un-escapes the string value
back to real quotes — then walk `message.content` for `type=="text"` blocks and search the **clean**
text for your marker. Do NOT regex the raw file.

```python
for line in open(path, encoding="utf-8", errors="replace"):
    if "CALIB" not in line: continue            # cheap pre-filter
    obj = json.loads(line)                       # un-escapes the text value
    content = obj.get("message", obj).get("content")
    for b in (content if isinstance(content, list) else []):
        if isinstance(b, dict) and b.get("type") == "text":
            text += b.get("text", "")            # now quotes are real → json.loads works
```

**Bonus (pollution guard):** only `type=="text"` blocks are the assistant's prose. **Tool inputs**
(Bash commands, Edit content, tool previews) live in `type=="tool_use"` blocks → reading only text
blocks means example/illustrative markers you typed into a *command or file edit* are NOT captured,
only markers in real chat prose. Verified: dry-run over a live transcript captured 0 from 14 `CALIB`
mentions (12 tool_use ignored, 2 illustrative `{...}` placeholders failed json.loads). Schema
(`type`/`message.content[]`/`text`) is **undocumented** by Claude Code — confirm it empirically, and
keep the hook best-effort (any failure → exit 0, never wedge a turn).
