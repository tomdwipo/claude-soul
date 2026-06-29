# Extract intent — don't echo the user's raw message into a structured field

**When this applies:** a skill/search/tool needs a **structured field** (persona, query, keyword,
parameter) and you're deciding how to fill it from a user's chat message.

**Principle:** **extract** the intent from the message through one processing step (LLM extract / parse /
normalize) *first*. **Don't** grab the raw message as-is and stuff it into the field — even when it "looks
good enough". Echo is a time bomb: it works when the user happens to type something complete, and shatters
when they type something terse. Raw input = a human's intent; the field = the shape downstream needs. The
bridge is **extraction**, not a copy.

**Why:** a production intent-capture step took the user's next message **verbatim** as a persona
(`persona = msg[:500]`). One user replied *"I want a remote job"* → that became the persona → the worker
derived keywords from a thin persona → failed → fell back to searching the **literal** string *"I want a
remote job"* on the listing source → garbage results. Another user succeeded **only because** they happened
to type a full persona in one message. A correct system must not hang on the luck of the user's phrasing.
The same root showed up twice in one feature: (1) echo the raw message → field; (2) **fallback echo** — when
keyword extraction failed, the fallback re-used the raw persona text, so it searched the *applicant's* words
instead of the *producer's* listing language.

**How to apply:**
- Before enqueue/search/dispatch: run an **extract step** (LLM summarize → JSON, or a parser) that turns
  the chat (+ artifacts: a CV, a profile) into structured fields. The raw message is **raw material**, not
  the result.
- Provide a **safe fallback, not an echo**: if extraction fails or is thin → ask for clarification / degrade
  gracefully (and don't charge for it). Never search raw text. A garbage search is worse than "nothing found
  yet, can you say more?".
- **Add an eval** on the extraction side: `rich` (the field is built from real signal) + `not_echo` (the
  field ≠ a verbatim copy of the input). Unit tests check plumbing and miss echo; a behavior eval catches it.
- Signals that arrive late (an artifact uploaded *after* the trigger) → pull them at the **point of
  consumption** (the worker reads the latest artifact), not only at the trigger point — inter-message races
  are real.

Related: [[eval-engineering]] (measure behavior, don't just coach), [[dont-expose-the-recipe]]
(different concern: don't reveal the engine to the user).
