# A feature-filter verdict is provisional until you pull behavioral telemetry — discovery can flip it

**When this applies:** running a decision filter over candidate features; judging "worth building / not
yet"; deciding whether discovery is needed first or you can build directly.

**Principle:** a filter verdict produced **before** you pull behavioral evidence is **provisional**, not
final. The same candidate can move between "discovery first" and "build" **purely** because you have (or
haven't) opened the telemetry. So before you rule: **pull the behavioral signal that already exists** (chat
logs, funnels, runtime events) — don't judge from imagination or assumption. If the first verdict is "not
yet," check whether it's genuinely "no need" or merely "I haven't looked at the data."

**Why:** a candidate feature went through a decision filter and got "discovery first" on the first pass —
reason: "no behavioral signal." As soon as a discovery pass pulled the usage logs, it turned out the
requested mode was actually the **dominant request pattern** (multiple real users had typed it explicitly).
The verdict jumped straight to "build." What changed was **not the candidate** — only "have I looked at the
data or not." Stop at the first verdict and a strongly-demanded feature gets skipped; build without pulling
data and you can build something nobody wants. Both failures come from the order "rule first, data later."

**How to apply:**
- **Telemetry BEFORE the verdict, not after.** Ahead of the filter, run the generator/discovery step that
  pulls real signal (usage logs, funnels, run records). Only then score.
- **Treat a "no/not yet" verdict as a hypothesis** until checked against behavioral data. Ask: "is this
  genuinely no demand, or have I just not opened the logs?"
- **Record the transition in the artifact** (e.g. "discovery-first → build after pulling usage logs") so
  the decision trail is honest — not pretending you were certain from the start.
- This is the *operational* side of [[discovery-before-prioritization]] and parallels [[eval-engineering]]
  (measure, don't guess) plus [[current-state-overrides-stale-memory]] (trust actual data, not memory).
  Behavioral evidence beats stated intent.
- **Eval-case (regression):** trigger "ruling on a feature without opening available telemetry" → correct
  behavior = pull logs/funnel first, then score; **wrong** = emit a final verdict from assumption when the
  data is right there to query.
