# Ground a claim in literature only when it's EMPIRICAL + general — a citation on a judgment call is false authority

**When this applies:** you're tempted to attach a paper/citation to a principle, doc, or claim to make
it look rigorous — or deciding whether the new paper MCP (the OpenAlex research MCP) should "strengthen" an
existing principle.

**Principle:** literature is legitimate evidence for **empirical, general** claims (LLM/agent behaviour,
methodology, measurable facts checkable against research) — for those it's a real **level-3** source on
the evidence ladder ([[verify-uncertain-claims-against-trusted-source]] #52). But for
**judgment / taste / in-project-incident** claims, the **incident or correction IS the evidence**; a
citation there is **false authority** — it invites cherry-picking (a paper exists for almost any
position), misattribution (the paper may not say what you claim), and it *dilutes* the real "why"
(the incident). Most principles in a workspace are the second kind → **do not paper-back them.**

When a principle DOES make an empirical claim from a **weak source** (vendor blog, a remembered
number), upgrade it to peer-reviewed **or caveat it as unverified** — don't leave a specific number
sourced to marketing. And remember the retrieval itself isn't trustworthy raw: keyword + citation-sort
returns topically-wrong, high-citation noise on niche/new topics, so **verify topic relevance
per-record** ([[openalex-evidence-verify-per-record-not-by-source]]).

**Why:** 2026-06-29 — installed the OpenAlex MCP for evidence-grounding and was tempted to back the
workspace's principles with papers. Reality: only a few make checkable empirical claims. **#7
eval-engineering** cited vendor-blog numbers ("LLM-judge ~66–70%, SME→95%"); the checkable part was
grounded to peer-reviewed **MT-Bench** (66–85% by setup) and the **"95%" flagged as unverified**. A
`type:review` search for "LLM-as-a-judge reliability" returned a **Cochrane review on borderline
personality disorder** as the top hit (citation-sort favoured old, heavily-cited, vocabulary-overlapping
clinical literature) — proof that a confident-looking citation can be topically absurd.

**How to apply:**
- Classify the claim first: **empirical+general** (→ literature is fair game) vs **judgment / taste /
  this-project incident** (→ the incident is the evidence; a paper is theater). When unsure, the "why"
  stays the incident.
- A specific empirical number from a weak source → upgrade (peer-reviewed) **or** caveat
  ("vendor claim, unverified"); never launder a marketing number into a fact.
- Read the actual finding, don't trust the abstract/citation-count: follow the OA link (HTML →
  WebFetch; PDF → download + vision `Read` for faithful tables/formulas).
- One supporting paper ≠ settled — look for the refuting work (#52 disconfirmation), and verify each
  record's topic relevance + internal metadata consistency before citing.
