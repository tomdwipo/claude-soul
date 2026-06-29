# Calibration loop

Measures whether Claude's stated confidence matches reality. A label like `[High]` is just a
feeling until something checks it — this records each material factual claim and, when ground
truth later surfaces, scores whether the label held. Closes the gap flagged in
[`../principles/verify-uncertain-claims-against-trusted-source.md`](../principles/verify-uncertain-claims-against-trusted-source.md)
(#52): provenance makes a claim *auditable*; calibration makes the *confidence label* accountable.

## The record

One row per claim (`log.jsonl`, one JSON object per line):

```
{id, ts, session, claim, confidence(High|Medium|Low), provenance, verdict(null|correct|wrong|partial), checked_ts, note}
```

`verdict: null` = not yet checked. It gets filled later, when a test / curl / user correction
settles whether the claim was true.

## Auto-capture (the `Stop` hook)

Logging is automatic via a marker, so you don't run `calib.py log` by hand. When you make a
**material** factual claim, emit a machine-readable marker right after it in your output:

```
...the chat model is pinned to sonnet-4-6 [High] (checked .env)
<!--CALIB {"claim":"chat model pinned to sonnet-4-6","confidence":"High","provenance":".env"}-->
```

On every turn the `Stop` hook (`.claude/calib-capture.sh`) reads the transcript, extracts these
markers, and appends new ones to `log.jsonl` (deduped by content hash — re-scanning the whole
transcript each turn never double-logs). **Only emit a marker for a claim worth tracking** — the
marker IS the materiality gate; spraying markers on every sentence floods the coverage metric and is
the failure mode this design avoids. **Verdict stays manual** — auto-capture removes the log step,
NOT the verify step. It does not make calibration autonomous.

## Workflow (for Claude, every session)

1. **Capture** = emit a `<!--CALIB {...}-->` marker on a material claim (auto-logged by the Stop hook).
   Manual fallback still works: `python3 .docs/calibration/calib.py log --claim "..." --confidence High --provenance "(checked .env)"`
2. **Fill the verdict** the moment ground truth appears — a test result, a curl, the user
   correcting you: `python3 .docs/calibration/calib.py verdict k007 wrong --note "only index row loads"`
3. **Open items** worth chasing: `calib.py list --open`
4. **Report**: `calib.py report` — accuracy per confidence level + a coverage warning.

## The honest catch (read this before trusting any number)

The hard part isn't the table — it's **verdict-fill**. Most claims never get a clean verdict, so
the sample skews toward claims that happened to be checked. `report` therefore prints **verdict
coverage** and, below 50%, refuses to present the accuracies as reliable — it warns instead of
pretending sparse, biased data is signal. Treat the numbers as directional only until coverage and
per-level sample size (≥5) are real. This tool was built **on the user's call, against the standing
recommendation to defer** until that coverage exists — so the guardrail is the point, not a footnote.

## Target shape of a well-calibrated record

`High` ≈ ≥85% correct · `Medium` ≈ 55–75% · `Low` ≤ 50%. If `High` runs well below 85%, that's
overconfidence → downgrade Highs and verify more before asserting.
