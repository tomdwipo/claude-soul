# One content source, many surfaces → placement flags + optional fields (progressive), NOT a per-surface fork

**When this applies:** the same content must appear on **more than one surface** (e.g. a hero showreel + a
feature section on a landing page; or web + mobile + email) with **different placement / depth** (surface A
shows item X, surface B doesn't; surface A is a short version, surface B is the full one).

**Principle:** **don't make a separate array/copy per surface** (twin sources = drift: edit one, forget the
other). Use **ONE data source**, then:
1. **Per-item placement flags** with sensible defaults (`hero`/`feat`, absent = `True`) → each surface just
   does `filter(flag !== false)`. Placement is metadata on the item, not a new structure.
2. **Optional fields for richer versions** (progressive enhancement, e.g. a multi-turn `chat[]`) read by the
   *same* surfaces through one code-path, with a **fallback** when the field is absent
   (`chat ? seq = chat : seq = [ask, reply]`). Adding the field to another item auto-upgrades it, **zero code
   change**.

**Why:** a landing page needed one item **added** to the hero **and** a clip **swapped** in the feature
section, while both renderers were driven from the **same** source list. Building two arrays (hero vs feature)
would be a twin copy — changing the item's text means editing two places → drift. The fix: a `hero`/`feat`
flag per item + an optional `chat[]` field that **both renderers read**, with a single-turn fallback for
items that don't have it. Result: one source, two different placements, one conversation reused across both
surfaces — and adding a richer variant later is just appending the field, no JS touched.

**How to apply:**
- **Default flag = include** (`get("feat", True)`) → old items need no change when you add a new flag concept
  (backward-compatible).
- **One code-path reads the optional field + fallback** — don't branch per surface; the difference is data,
  not logic.
- **Test placement explicitly:** assert a hero-only item does NOT appear on the other surface (the absence),
  not just that present items render. A silently-missing item is the easiest bug to pass.
- **Selective progressive:** add the rich field only to items that need it; the rest fall back (don't force
  everything into the rich shape). Reuse one conversation source across surfaces
  ([[recreate-live-animation-deterministically]]).
- **Eval-case:** "same content, different placement/depth per surface" → correct = 1 source + flags +
  optional field + fallback; **wrong** = per-surface array/copy (drift) or per-surface code branches
  (duplicated logic).

**Same mechanism (project from ONE source of truth; a hand-maintained parallel copy drifts):**
[[derive-agent-capabilities-from-registry]] — an agent's prompt/capabilities assembled from the registry,
not a hardcoded list. Different artifact (multi-surface content vs agent self-knowledge), same anti-drift.
