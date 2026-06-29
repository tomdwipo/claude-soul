# Store the external response WHOLE (not a mapped subset) when the data feeds a moat/eval
**When this applies:** wiring an external data source (API/scraper/actor) whose data is **not only for the
current task** but also feeds the product moat / eval / future features (a data flywheel: accumulate data
+ labels from the first user).

**Principle:** persist the **raw response as-is (all fields)**; map only for the immediate pipeline. The
mapped subset is **lossy & irreversible** without fetching/paying again. Store the raw-whole, derive lossy
views on top — never overwrite the raw.

**Why:** the first design instinct is to store only the mapped result (the few fields the current pipeline
needs). But the rich fields you drop now (author, full stats, media, hashtags, ids) **can't be recovered
later** without paying the source again. Disk is cheap; re-fetching isn't; a dropped field is gone. For
eval-as-moat, the raw is irreplaceable raw material ([[eval-engineering]]).

**How to apply:**
- **Default to a raw artifact file** (e.g. `raw.json`) → the DB stays lean; promote to a **table** (1 row/item, dedup by id) only when you need cross-run query/dedup (YAGNI until the data justifies it).
- **Label what you discarded too** — keep a flag (passed_filter? became_output?) so negatives are labeled (eval material for the filter).
- **Mapping is separate, never overwrite raw** — the pipeline view ≠ the source of truth.
- **Return `(mapped, raw)`** — a fetch function returns the original item too, not just the squeezed version.
- Pairs with [[probe-contract-before-integrating]] (know the real fields first), [[dont-expose-the-recipe]].
- **Eval-case:** trigger "wiring an external API into a moat/eval product" → correct = persist raw whole + derive views; **wrong** = store only the mapped/filtered result.
