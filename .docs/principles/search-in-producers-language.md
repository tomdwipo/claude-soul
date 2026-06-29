# Search in the PRODUCER's language, not the seeker's — unstructured = a source, not a defect
**When this applies:** building search over an unstructured corpus (social posts, documents, listings) to
**find items** matching a target (openings, demand, leads, answers). When composing keywords/queries.

**Principle:** derive keywords in the **language the content's PRODUCER uses**, not the seeker's
self-description. A seeker says *"I can do admin, Excel"* — but the producer of a listing writes *"admin
wanted / now hiring / open role."* Raw seeker words = an ocean of non-targets; pair **role × producer-intent
words**. Corollary: for informal/unstructured sources, the source is **not low quality** — your value-add is
**filter → extract → match**, not wishing for clean data.

**Why:** unstructured posts are often *exactly* where the informal version of what you're looking for lives,
and producers almost always include a way to act (apply/contact). Keyword quality = the recall ceiling.
Searching the seeker's word floods you with non-target content; searching the producer's phrasing finds the
real items. Evidence comes from a real sweep: natural producer phrasing catches targets that rigid tags miss.

**How to apply:**
- **Keyword-derivation = its own step** (tunable, evaluable), not buried in a chat prompt. Run it **after**
  context is complete, output producer-language phrases (role × intent-word [+ facets like location/mode]), capped in count.
- **Pipeline = over-fetch → filter (is this really a target?) → extract → match**, because even
  producer-words carry noise; over-fetch counters filter-loss.
- **Sharpen via stored data** — which keywords actually hit real targets → improve the derivation prompt (eval flywheel, [[store-raw-complete-for-flywheel]]).
- Pairs with [[discovery-before-prioritization]] (don't jump to solutions; here, don't jump to the seeker's word), [[calibrate-to-the-real-audience]].
- **Eval-case:** trigger "build search over an unstructured corpus to find X" → correct = producer-language query + filter/extract/match pipeline; **wrong** = search with the seeker's raw self-description.
