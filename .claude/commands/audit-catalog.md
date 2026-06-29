# /audit-catalog — periodic by-mechanism audit of the .docs catalogs (dedup / cross-link / drift)

Run a SYSTEMATIC, exhaustive audit of `.docs/common-issues/` (default) — or `.docs/principles/` if
`$ARGUMENTS` says "principles" (or "both"). Cross-session catalogs accrete overlap, broken links, and
doc↔code drift that incremental passes miss; this finds them in one pass. Common-issues need this more
often than principles (raw incidents vs distilled-via-how-to-learn).

**Why a command, not a cron:** findings need judgment to act on (which links are genuine, what to skip),
so this runs with review, not autonomously. Invoke it periodically (e.g. every ~15–20 new entries, or
after a big feature batch).

## Method (the lesson this encodes)
Scan by **MECHANISM, not by label** — the same gotcha filed under a different topic label hides from a
keyword grep and from a skim. And run a **disconfirmation pass**: don't stop at the comfortable "it's clean."

## Steps
1. **Extract mechanisms (delegate, fresh).** Spawn a fresh general-purpose sub-agent (independent →
   no bias from prior conclusions). Have it: list every `.md` in the target dir (excl. `README.md`,
   `how-to-learn.md`, `android/`); read EACH and write its **core mechanism** in one line (the cognitive
   move, independent of topic/stack); group by shared mechanism; for each group ≥2, grep members for
   `[[other-slug]]` to see what's already linked. It must report, conservatively:
   (a) same-mechanism clusters with a MISSING cross-link (members + which links absent),
   (b) true near-duplicate / merge candidates,
   (c) **broken wikilinks** (a `[[slug]]` whose file doesn't exist),
   (d) counts (files read, distinct mechanisms). Read-only; tag each finding [High/Med/Low].
   Tell it which clusters are already-linked (exclude them) so it doesn't re-report.
2. **Verify each candidate yourself by READING the files** — never link on the sub-agent's abstraction
   alone (a one-line mechanism can over-group). Confirm the cognitive move genuinely matches.
3. **Cross-link the genuine ones, don't merge** — each entry keeps its specific "how"; add a one-line
   "shared mechanism" note + bidirectional `[[ ]]` links (+ a sibling-ref in the index row for recall).
   Merge only a TRUE duplicate (one fully absorbs the other) — rare; merge ≠ free.
4. **Fix broken wikilinks** (slug typos) and **repair drift on sight** — if an entry describes a state
   that now contradicts the code (e.g. "we kept X loose" but X was since fixed), update it
   (doc-tracks-code). The by-mechanism read surfaces drift a label-skim never would.
5. **Be conservative — skip loose ones, say so.** Don't mechanically link every thematic adjacency
   (over-linking dilutes recall too). If a cluster's real home is an existing principle, point each
   member at the principle instead of peer-linking.
6. **Idempotent:** re-running is safe — already-linked pairs are excluded, edits are additive. If a
   parallel session may have touched the catalog, `git fetch` first.
7. **Log + review:** add a dated `recent-updates` line (clusters linked, drift/broken-links fixed, what
   was consciously skipped + why). Show the diff and STOP for review; commit only when told. Propagate
   generic findings to a public mirror if one exists (if a public mirror exists); note any cluster whose member isn't there.

Pairs with the Unified Save Protocol ("scan first — by mechanism") in `.docs/common-issues/README.md`
and the doc-tracks-code principle (fix drift on sight).
