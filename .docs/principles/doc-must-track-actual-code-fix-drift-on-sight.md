# Docs/system-design MUST track the actual code/prod — found drift = fix the doc on the spot, not just "don't trust the doc"

**When this applies:** as-built / system-design / architecture docs (C4, ERD, runtime-flow, "live status")
that **describe real system behavior** — flags, sandbox/headless mode, model, tables, routes, phase status.
The moment you're reading/verifying prod and find a doc that **contradicts** the actual code/config/prod.

**Principle:** a stale doc is **not neutral — it ACTIVELY misleads** the next reader (including future-you,
a teammate, and any lookup-first agent that gets fed it each session). So once drift is **confirmed**
(verify, don't accuse), **fix the doc immediately** — ideally in the same change-set, before moving on.
"Don't trust the doc, trust the disk" is only half; the other half is **REPAIR the doc so others don't
fall in the same hole**. Standing rule: **system-design must align with the actual code**; when code
changes, the doc follows BEFORE commit (the ritual: file-level + alignment table + date). A doc lagging the
code is a bug, not a later chore.

**Why:** an as-built doc's "honest status" block claimed the chat ran in a headless, tools-off, dark mode
with the sandbox flag off — when prod had long been running in sandbox mode with tools on. The doc even had
a "CORRECTION: actually live" note, but the stale text was **left dangling below it** → self-contradictory.
The result: people (and this agent early in the session) built a wrong mental model of prod, which leaked
into feature design (injection points, model assumptions). It only surfaced on a **live probe**. Twist: the
first probe used the *host binary* and reported one model — written down as "the prod model" — but the real
chat runs in a *sandbox image* defaulting to a different, more expensive model; that only surfaced when a
provenance feature persisted the model from the actual run. So even the first correction was still drift —
the deeper lesson: **"verify" must be on the EXACT runtime path** (the sandbox image), not a "similar" one
(the host binary) ([[validate-in-real-runtime-context]]). Once proven, the doc was corrected right away
(header block + table row + README + memory), not "later." Stale/near-miss docs left alone are repeat traps.

**How to apply:**
- **Drift confirmed → fix the doc now**, not by stacking an "FYI this is no longer accurate" note on top of
  old text you leave in place (that's exactly what made the doc contradictory). Delete or mark-as-historical
  the stale text; don't pile on.
- **Same change-set when possible:** change code → update doc + alignment + date before commit. The doc
  isn't chased afterward.
- **Verify before you correct** (don't accuse) — read the actual code/config/prod ([[validate-in-real-runtime-context]]);
  for any LIVE claim (model/flag/runtime) that can change, read from a source that can't lie (the live
  response, a schema/PRAGMA query, the service manager), not memory or the doc.
- **Log it in the alignment ledger** even for doc-only changes — so the correction is traceable.
- Companions: [[current-state-overrides-stale-memory]] (current-state beats the stale — this is its REPAIR
  side), [[erd-tracks-schema-changes]] (ERD must match the live DB), [[validate-in-real-runtime-context]]
  (verify on the real runtime), [[feature-must-land-on-the-prod-path]] (check the prod branch actually runs it).
- **Eval-case:** trigger "found an as-built doc contradicting actual code/prod" → correct = verify → fix doc
  + alignment in that change-set, stale text removed/marked historical; **wrong** = just "don't trust the
  doc" with no repair / stacking a correction note on top of old text (contradictory) / deferring the doc
  update to "later."
