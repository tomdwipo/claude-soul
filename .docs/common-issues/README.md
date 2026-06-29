# Common Issues — Catalog

Deterministic **rules**: gotchas a compiler / test / lint / build result can settle. (Judgment
calls go to [`.docs/principles/`](../principles/README.md) instead.) Version-controlled so every
session inherits them.

> **Scope:** workspace-wide entries that apply across project types live here. A gotcha that only
> matters inside one sub-project belongs in *that* sub-project's own `.docs/common-issues/`.

## Unified Save Protocol (follow before adding anything)

1. **Scan first — by MECHANISM, not one keyword.** The same gotcha filed under a different label
   (e.g. `subprocess/venv` vs `subprocess/PATH`) hides from a single-keyword grep → you create a
   sibling that's really a duplicate (and a later audit skimming by label misses it too). Grep a few
   *mechanism* words, skim adjacent subjects, and **reuse an existing sibling's label** so the next
   scan finds it. If a related chapter exists, append a **dated sub-note** rather than a sibling file.
   When *auditing* the catalog for dups, compare by mechanism and run a disconfirmation pass ("what
   overlap am I NOT seeing?", [[verify-uncertain-claims-against-trusted-source]] #52) — don't stop at
   the first comfortable "it's clean."
2. **One fact per file** — new chapter = new `kebab-case.md`; keep it small and specific.
3. **Register it** — add a row to the index below **and** a one-line pointer in the §Common Issues
   section of the root [`CLAUDE.md`](../../CLAUDE.md) if it's load-bearing.
4. **Commit tight** — the catalog change ships in the same commit as the fix that taught it.

## Index

_(empty — first real gotcha lands here. Group by subject as the catalog grows, e.g. `build`,
`ci`, `testing`, `networking`, `<language/stack>`.)_

| Subject | Entry | Summary |
|---------|-------|---------|
| git / security | [gitignore-secrets-before-first-push](./gitignore-secrets-before-first-push.md) | Gitignore secret-bearing files (e.g. `.mcp.json`) before the first commit/push; rotate if leaked |
| shell / file-ops | [cp-into-existing-dir-nests](./cp-into-existing-dir-nests.md) | `cp -R src dst` nests inside dst if dst already exists; use `cp -R src/. dst/` to merge contents |
| shell / zsh | [zsh-no-word-split-unquoted-var](./zsh-no-word-split-unquoted-var.md) | zsh does NOT word-split an unquoted scalar → `for f in $LIST` / `cmd $CMD` runs ONCE over the whole string (bash splits, zsh doesn't); symptom = "File name too long" / silent no-op. Use `bash -c '…'`, `${=LIST}`, or a real array. A `2>/dev/null \|\| echo ok` can mask the collapse — print a per-item line to confirm it iterated |
| hooks / claude-soul | [pretooluse-gate-matches-substring](./pretooluse-gate-matches-substring.md) | `learn-gate.sh` matches the substring `git commit`, so it fires on any Bash call containing that text; escape via the no-lessons marker or stage a learning first |
| hooks / transcript-parse | [transcript-jsonl-text-is-escaped-json-string](./transcript-jsonl-text-is-escaped-json-string.md) | A hook reading `transcript_path` to extract assistant text/markers finds **0** if it greps the RAW file: text is stored AS a JSON string → quotes arrive escaped (`\"`) → `json.loads` fails. Parse the JSONL line-by-line (un-escapes) → read `content[]` `type=="text"` blocks. Only text blocks are prose, so markers in tool_use (Bash/Edit) are safely ignored. Schema undocumented → verify empirically; best-effort (fail→exit 0) |
| hooks / stop-timing | [stop-hook-runs-before-transcript-flush](./stop-hook-runs-before-transcript-flush.md) | A `Stop` hook acting on the just-finished turn may run BEFORE the transcript flushes → scans a transcript one turn stale, misses its trigger marker (caught next turn). Fix: re-scan the WHOLE transcript each turn + dedup by content hash → eventually-captured ≤1-turn lag. Don't assume same-turn; **don't** optimize to "last message only" (flush race → permanent loss). Best-effort (fail→exit 0) |
| research / openalex-mcp | [openalex-evidence-verify-per-record-not-by-source](./openalex-evidence-verify-per-record-not-by-source.md) | OpenAlex MCP kills *fabricated* citations but per-record metadata can be **conflated** (title of one paper + DOI/authors/abstract of another). Verify DOI↔title↔authors↔abstract **per record**, don't blanket-filter by `type`/source: preprint≠arXiv (bioRxiv/SSRN/Research Square), most arXiv records are clean, "find the published version" is unreliable. Keyword+citation-sort returns off-topic high-citation noise on niche topics. MCP returns abstract+link; body via WebFetch (HTML) or download+vision `Read` (PDF). Citation count ≠ truth |
| testing / verify-ordering | [confirm-positive-signal-before-teardown](./confirm-positive-signal-before-teardown.md) | A verification that prints **nothing** is *unknown*, not a pass — usually a harness bug, not the thing under test. Assert the EXPECTED positive marker (`31 tools`, `healthy`), never "no error". **Don't teardown** the dummy/clone/temp until the pass is confirmed — else a false-negative destroys the artifact you'd debug with. Trust the output, not the exit-code; zsh mechanics → [zsh-no-word-split-unquoted-var] |
