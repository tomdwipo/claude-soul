# A public mirror of a private source-of-truth drifts BOTH ways — reconcile back, don't only push forward

**When this applies:** you maintain a **public mirror/template** (OSS repo, shared template) derived from a
**private source-of-truth** (the workspace that feeds every session). Over time both get edited — the private
one in daily work, the public one during cleanups, README polish, or content authored *directly* in the
mirror.

**Principle:** sync between a mirror and its source is **bidirectional**, not a one-way push. The natural
mental model — "private is upstream, public is a downstream copy" — is wrong the moment anyone authors
content **directly in the mirror** (a generic principle written straight into the public repo, a README claim,
a fix). That content must be **reconciled back into the source**, or the source — the thing that actually
gets loaded every session — silently falls behind its own public face. Before treating "are we in sync?" as
"did we push everything out?", **diff both directions** and pull the mirror-only items home first.

**Why:** auditing a public soul-template against its private source found drift **both ways**: 5 private
principles not yet pushed out, AND **3 principles that existed only in the public mirror** — authored generically
during a backport and never reconciled back. The source-of-truth, which feeds context every session, was
missing three of its own principles. A one-way "push the new stuff out" pass would have left that gap open
forever, because it never looks at what the mirror has that home doesn't.

**How to apply:**
- Sync = a **two-way diff** (`comm -3` both lists), not a push. List mirror-only AND source-only items.
- **Reconcile the mirror-only items into the source FIRST**, then push source-only items out — home is the
  authority that gets read every session ([[current-state-overrides-stale-memory]]).
- When you author something *directly* in the mirror (quick generic write-up in the public repo), leave
  yourself a reconcile step — it isn't "done" until the private source has it too.
- **Mechanism drifts too, not just content.** The mirror can hold *enforcement machinery* (a gate script,
  a git hook, its eval) that the source never had — the source kept the principle but not the thing that
  enforces it. Diff scripts/hooks/config, not only `.docs/` markdown; back-port the mechanism so the source
  actually *runs* the discipline it documents, instead of relying on manual recall.
- Pairs with [[genericize-private-content-before-public-push]] (the outbound leg) and
  [[name-conflicts-with-source-of-truth]] (the source is the authority).
