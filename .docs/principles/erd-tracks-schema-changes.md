# A schema change isn't done until its ERD matches the live database
**When this applies:** any change that touches persistence — a table/column/relation/index, an ORM
entity/DAO/migration, or a SQL model. Covers planning, breakdown, and landing.
**Principle:** the data-model diagram (ERD) is a **deliverable of the schema change, not optional
documentation**. Treat it like the flow diagram or the screenshot baseline: plan its delta, update
it when the change lands, and **verify it against the real schema — never from memory or the model
file alone**. A diagram that can silently drift from the database is worse than none, because it
reads as truth.
**Why:** a model file and the live DB diverge whenever migrations lag — many ORMs' "create tables"
step won't ALTER or DROP existing columns. So a prod table can carry dead columns that were removed
from the model long ago, and a *model-derived* ERD will quietly hide that drift in a footnote. The
durable fix isn't a one-off redraw: it's a generator that introspects the **live** DB and reports
model↔DB drift, so the diagram can be *regenerated and verified* (drift: none) instead of hand-trusted.
**How to apply:**
- **Prefer generated over hand-drawn.** Where a schema generator exists, it is the verification source —
  the AFTER ERD must match its output and report no drift. If none exists and the schema is non-trivial,
  building one is usually worth more than redrawing.
- **Verify against the *physical* schema, not the model file.** Model ≠ DB when migrations lag; drift hides exactly there.
- **Locate the canonical ERD** (nearest data-model doc); if absent, the change *creates* it. Keep it in the same format as the rest of your architecture docs.
- **No-DB-change → say so**: `ERD: N/A — no database change`, never silently omit.
- Pairs with [[adapt-template-to-stack]] (translate the gate to the stack) and [[validate-in-real-runtime-context]] (the live DB is the runtime truth, not the model source).
