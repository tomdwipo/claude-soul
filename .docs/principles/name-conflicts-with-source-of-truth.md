# Verify a source-of-truth "conflict" is real before flagging it
**When this applies:** a new direction looks like it diverges from a source-of-truth doc (foundation,
PRD, ADR, "if conflict this wins" doc).
**Principle:** first confirm it actually contradicts the **same dimension** the doc speaks to. A new
layer the doc never addressed is not a conflict — it's an addition. Only a genuine same-dimension
clash gets flagged: then name it openly and align the doc. Never silently contradict, and never
manufacture a false alarm.
**Why:** it's easy to read an ambiguous doc statement, decide a new design "violates" it, and slap a
⚠️ "changes the source doc" banner on something that was never in conflict. Example shape: a doc says
"component X runs on the user's device"; you add a *separate* component Y that runs on a server and
flag it as contradicting the doc. But the doc spoke about X's location, not Y's — different dimension,
no conflict. The false alarm costs trust and churn.
**How to apply:**
- Pin down WHICH dimension the doc statement is about vs WHICH you're changing. Different dimension →
  not a conflict.
- If the reading is ambiguous, ask the user which they meant before declaring a contradiction.
- When it IS a genuine same-dimension clash, name it side by side + update the source doc to align —
  don't leave two docs quietly disagreeing.
- Pairs with [[catalog-lookup-every-first]]: look up first, then read precisely before reacting.
