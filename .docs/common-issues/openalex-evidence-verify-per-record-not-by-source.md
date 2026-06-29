# Grounding citations via the OpenAlex MCP: verify per-RECORD, don't filter by source/type — and don't rely on "find the published version"

**When this applies:** using the `openalex` MCP (or OpenAlex directly) to ground a paper/scientific
claim in real evidence instead of citing from memory.

**Setup (it isn't shipped — `.mcp.json` is gitignored):** copy the `openalex` block from
[`.mcp.json.example`](../../.mcp.json.example) into your project's `.mcp.json` (`npx -y
openalex-research-mcp@0.5.0`, set `OPENALEX_EMAIL` to your own; pinned version = supply-chain safety),
then restart the session so the MCP loads. It's read-only and needs no secret (OpenAlex is keyless).

**What it fixes / what it doesn't:** querying OpenAlex kills *fabricated* citations (you get real,
pointable records) — it does NOT verify the *validity of a finding*, and its **per-record metadata
can be wrong**. Treat retrieval as "real candidates," not "true facts."

**The traps (all seen live):**
1. **Conflated / "frankenstein" records.** A single OpenAlex work can carry the title + arXiv id of
   one paper but the **DOI, authors, and abstract of a different one** (preprint dedup/merge error).
   Example: a record titled "GPT-4 Technical Report" had DOI `10.4230/lipics.cosit.2024.11` (a COSIT
   *geography* conference), authors from Massey/Cardiff, and an abstract about an unrelated "MFOUR
   Vibe Framework." Citing its DOI/authors = propagating a corrupt citation.
2. **`type:article` is the wrong axis.** It drops **all** preprints — but **preprint ≠ arXiv**
   (bioRxiv, medRxiv, SSRN, Research Square, etc. are preprints too; a clean Research Square record
   got wrongly excluded). And **most arXiv records are fine** — blanket-excluding arXiv throws away
   canonical clean papers (e.g. the MT-Bench LLM-as-judge paper, whose arXiv record is correct).
3. **"Find the published version" is unreliable.** For many ML papers OpenAlex keeps everything on
   the **arXiv preprint record** (it holds all the citations); the conference/journal version often
   isn't separately indexed, or is a near-empty stub. `get_work` on the preprint shows a single arXiv
   location. Title-search to find the published record matches loosely (token, not exact-title) and
   frequently fails. So you can't dependably swap an arXiv record for a published one.
4. **No "NOT source" filter** in the MCP (only positive `source_name`/`source_issn`/`source_id`). To
   exclude a source, over-fetch and drop it in your own post-processing (arXiv `source_id` =
   `S4306400194`).
5. **Keyword + citation-sort returns topically-WRONG, high-citation noise** on niche/new topics. A
   `type:review` search for "LLM-as-a-judge reliability agreement" sorted by citations returned, as the
   **top hit, a Cochrane review on borderline personality disorder** — clinical literature is dense in
   "reliability/agreement/inter-rater bias" vocabulary and has decades of accumulated citations, so it
   buries 2023+ niche topics. Don't `sort:cited_by_count` for a *new* topic; prefer relevance sort
   (default), `exact_phrase`, or topic/field constraints — and **verify each record is actually on-topic**
   before trusting it.

**The right workflow:**
1. Query **broad** — don't blanket-filter by `type` or source.
2. **Per-record metadata sanity-check**: is DOI ↔ title ↔ authors ↔ abstract internally consistent?
   Drop the garbled record regardless of source; keep clean ones (arXiv/preprint/article all OK).
3. To read the *finding* (not just metadata), follow `oa_url`/`pdf_url` — the MCP returns the
   **abstract + a link**, not the body. Two ways to get the body: **HTML full-text → WebFetch** (fast,
   targeted, but lossy on PDFs); **PDF → `curl` download + vision `Read`** (faithful for multi-column /
   tables / formulas, because it *sees* the page — better than text-extraction PDF tools that hit the
   same lossy layout problem; token-heavy, so target specific pages, max ~20/request). Paywalled (no OA
   copy) = body inaccessible — metadata/abstract only.
4. Citation count ≠ correctness; one supporting paper ≠ settled (cross-check, look for refutations).

**Evidence:** 2026-06-29 — grounding an "LLM-as-judge agreement" claim. Top arXiv hit was a
frankenstein record; `type:article` would have dropped a clean Research Square preprint; the MT-Bench
published version was unfindable (arXiv record is canonical). The MT-Bench abstract (verified via
`get_work`) gave a real number — GPT-4 judge ">80% agreement with humans" — which **corrected** a
"~66–70%" figure recalled from memory. Complements the OpenAlex research MCP and the evidence ladder in
principle #52 (verify-uncertain-claims): the MCP raises paper-evidence from memory (level 4) to a
pointable source (level 3), still below runtime/code for claims about *this* system.
