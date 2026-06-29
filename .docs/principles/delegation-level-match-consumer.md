# Match the delegation level to the consumer's reliability — default LLM-facing interfaces to "Tell"

**When this applies:** designing any interface a model/agent consumes (tool schema, skill manifest,
docstring, error message) — or a runbook/spec for a person.

**Principle:** the 7 levels of delegation (Tell → Sell → Consult → Agree → Advise → Inquire → Delegate)
measure how much *interpretation* you hand to the receiver. Every inference you require is a place a
weaker consumer can fail. **Default to "Tell":** hand the exact, copy-paste-ready action. Climb to higher
levels (give rationale / options / just the intent) **only** when the consumer is proven reliable enough
to fill the gap — or when over-specifying would shackle a capable agent.

**Why:** a "how to use" field that hands the model a raw sample and makes it reverse-engineer the call
format is high-inference and breaks silently when the sample is wrong for some cases. Replace it with a
literal, ready-to-run invocation string (Tell) and even a weak model just copies it — nothing to guess.
Generate that string from the manifest so it stays honest and zero-maintenance. A "broken-silently" stat
field is worse than no field.

**How to apply:** when adding a tool / field / interface, ask **"if a weak model read ONLY this, could it
act without guessing?"** If no → drop a level (give the exact invocation, not the format to infer). The
same lens applies to humans: a junior gets a Tell-level runbook, a senior gets a Delegate-level goal —
match the level to who's receiving. Pairs with [[tolerate-client-arg-coercion]] (assume clients are
imperfect, so spell it out) and [[calibrate-to-the-real-audience]] (design for the actual consumer, not the strongest one).
