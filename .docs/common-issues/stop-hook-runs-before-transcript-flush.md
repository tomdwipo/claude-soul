# A Stop hook can run BEFORE the transcript is flushed — re-scan the whole transcript + dedup, don't assume same-turn

**Symptom:** a `Stop` hook reads `transcript_path` to act on the **just-finished** turn (e.g. extract a
`<!--CALIB {...}-->` marker the assistant emitted) and **misses it** — the marker is clearly in the
chat, but the hook captured nothing that turn. The same marker IS picked up on the **next** turn.
(Evidence: the `calib-capture.sh` Stop hook captured the `reload` claim one turn, but the next turn's
`OpenAlex` marker only landed on the turn after — confirmed by a dry-run: the marker was absent from
the transcript when that turn's hook ran, present by the next.)

**Cause:** the Stop hook fires around the moment the turn ends, and the assistant's final message may
not be **flushed to the transcript JSONL yet** — a race between the transcript write and the hook
process. So the hook scans a transcript that's **one turn stale**: it's missing the very turn that
just triggered it.

**Fix / design rule:** make the hook **idempotent and re-scan the WHOLE transcript each turn**, then
**dedup** (content hash). A marker missed this turn (not flushed yet) is caught on the next turn's
re-scan, and dedup stops the already-captured ones from doubling. Net: **eventually-captured with
≤1-turn lag**, not same-turn. Two traps to avoid:
- **Don't assume same-turn availability** — anything keyed on "the turn that just finished is in the
  transcript now" is racy.
- **Don't optimize to "only the last message"** — that turns the flush race into **permanent data
  loss** (the missed marker is never re-scanned). The whole-transcript re-scan is what makes it
  self-healing; the dedup is what makes the re-scan cheap/safe.

Keep the hook best-effort (any failure → exit 0; a Stop hook must never wedge a turn). Pairs with
[[transcript-jsonl-text-is-escaped-json-string]] (the other transcript-reading gotcha: parse the
JSONL line, don't grep raw).
