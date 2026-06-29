# Current state = the authority that beats stale memory — don't fix it by deleting context
**When this applies:** a memory-bearing agent/assistant (chat, RAG, conversation history) whose
**capabilities/info change over time** — a new feature ships, pricing changes, a policy updates. When the
agent mimics an OLD answer that's now wrong.

**Principle:** if the agent once honestly said "not available / can't" and you then **ship that feature**,
the agent often **mimics the old memory** (refuses even though it can now). **Don't fix this by deleting the
user's context** — it doesn't scale (you can't reset every user's memory) and it throws away real history.
The fix: **make CURRENT STATE (the capability catalog / current info) the PRIMARY source of truth in the
prompt — ABOVE memory**. Memory is historical; if old memory contradicts current state, current wins, and
the agent tells the user "you can do this now."

**Why:** after shipping a feature, a user who earlier asked for it and got "can't yet" (honest then) can
still get refused — because the retrieved recent context injects the old refusal, so the model stays
consistent with its history. Deleting context isn't a real solution ("what about real users? delete every
person's context?"). The right fix: the prompt states the capability list is "what's available NOW, above
memory; if old memory says no but it's in the list now, the feature EXISTS — do it + say it's available now."
Result: it survives light poisoning and reframes to "Yes — this works now."

**How to apply:**
- **Mark current-state as authority in the prompt**, explicitly above memory: "this is true NOW, above history; history is only historical." Don't just say "ignore the old" — give a truth hierarchy.
- **Have the agent acknowledge the change**: "earlier it wasn't, now it is" > silent (more honest + builds trust).
- **Don't delete memory as a routine fix** — it's a band-aid, discards data, doesn't scale. Delete only for extremely poisoned test accounts.
- **Honest limit:** override beats light poison (1-2 old traces); poison that ACCUMULATES (dozens of refusals, embedded → retrieved) can outweigh the prompt → needs targeted memory refresh (e.g. invalidate stale traces when the catalog changes). That's separate complexity.
- Pairs with [[derive-agent-capabilities-from-registry]] (the catalog = capability source), [[eval-engineering]] (test the override against poisoned context, not just fresh).
- **Eval-case:** trigger "ship a new feature, a previously-refused user asks again" → correct = agent says "this works now" + does it; **wrong** = mimics the old refusal / "fix" is deleting context.
