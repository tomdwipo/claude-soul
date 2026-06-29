# system-design Command

Produce a **detailed system design** for $ARGUMENTS using **ASCII diagrams only** (no Mermaid, no
images — per workspace `CLAUDE.md`), with **BEFORE/AFTER** so the change is obvious. This is the
*architecture* artifact ("what it is shaped like + why"), the upstream input to `/breakdown-design`
(which turns it into step-by-step code). Keep them paired: same feature, same folder.

think hard. Ground every claim in the actual codebase (read the files first — see §Lookup First).
follow YAGNI — design only what the goal needs; no speculative components or dead structure.

## Output mode — ASK FIRST (this is the whole point of this command)

Parse $ARGUMENTS for an explicit mode flag:
- `--chat` (or the word `chat`) → render the full design **in chat only**, write no file.
- `--file` (or the word `file`/`md`) → write the design to a markdown file (see §File Location),
  then post a short summary in chat + the handoff line.

If **no mode flag is present**, ask the user ONCE with `AskUserQuestion`:
> "Where should the system design go?" — options: **Chat only** / **Save to .md file (ready for
> /breakdown-design)**.

Do not proceed until the mode is known. Everything else (the design itself) is identical in both modes
— only the destination differs.

## File Location (when mode = file)

Mirror `/breakdown-design` exactly so the two artifacts sit **side by side in one feature folder**:

```
.docs/YYYY/MM/DD/{NN}-{Feature-Spec}/{Feature-Spec}-system-design.md
```

- `YYYY/MM/DD` = today (from the session date).
- `{NN}` = next free 2-digit number in that day's folder (e.g. existing up to `13-…` → use `14`).
  **Reuse the SAME `{NN}-{Feature-Spec}` folder** if it already exists for this feature, so the later
  `{Feature-Spec}-implementation-plan.md` from `/breakdown-design` lands in the same folder.
- `{Feature-Spec}` = short Title-Case-Hyphenated name you infer from $ARGUMENTS.
- After writing, print the path + a one-line **handoff**: `Next: /breakdown-design <feature>` so the
  user can generate the implementation plan from this design.

## Lookup First (before writing anything)

This may be a multi-stack workspace. Before designing:
1. Find the nearest sub-project `CLAUDE.md` and adopt its stack, conventions, build/test command.
2. Scan `.docs/principles/`, `.docs/common-issues/`, the current month `.docs/recent-updates/YYYY/MM.md`,
   and the project's architecture doc (e.g. a `c4/` or `architecture/` folder). Open any file whose
   keyword overlaps the task. Design from what's already there — reuse > invent.
3. Read the real source files you'll reference so BEFORE diagrams reflect the code as it actually is
   (correct table names, function names, file paths, line numbers).

## Stack Adapter

The **universal spine always applies** (every stack). Android-only blocks are N/A elsewhere — write
`N/A — <stack> not Android, <reason>`. Map per nearest `CLAUDE.md`:

| Concept | Android (reference) | Python service | Node service |
|---------|---------------------|----------------|--------------|
| Test gate | `./gradlew … test` | `pytest` | `npm test` |
| Diagram code | Kotlin sketches | Python sketches | JS/TS (ESM) |
| Observability | Timber → Crashlytics | stdlib `logging` → log sink | `console`/stdout |
| Data store | Room `@Entity` | ORM model + DB | per project |
| Architecture doc | module docs | `c4`/architecture doc | architecture doc |

## Required Sections (the system design template)

Produce ALL of these, in order. **Every structural diagram is ASCII and must have a BEFORE and an
AFTER variant** (if a section genuinely does not change, write `AFTER: unchanged — <one-line why>`).

### 1. Context & Goal
- Problem in 2-3 plain sentences. What the user actually wants.
- **In scope** / **Out of scope (YAGNI)** — name what you are deliberately NOT building.
- Constraints discovered during Lookup (RAM/CPU limits, ToS, existing patterns, common-issues).

### 2. Design Decisions (table)
One row per real decision: **Decision · Chosen · Why · Alternative rejected**. This is where tradeoffs
live (e.g. "extend table vs new table", "local model vs API", "inline vs deferred"). Be honest about
the rejected option's downside.

### 3. High-Level Architecture — BEFORE / AFTER (ASCII)
Component/box diagram of the system slice this touches: entry points (HTTP/CLI/UI/queue/MCP), the
engine/modules, the data store, external services (LLM, queues). Mark **new** components clearly
(`◀ NEW`). Show how a request flows through boxes.

### 4. Data Model — BEFORE / AFTER (ASCII ERD)  ·  *only if persistence is touched*
ASCII ERD with entities/columns/relations. Mark `✅ NEW` / `⚠ CHANGED` columns. State relations
(note logical/in-code joins vs real FK). If no DB change: `Data Model: N/A — no persistence change`.
Name the migration reality for the stack (e.g. an ORM `create_all`/auto-create does NOT alter existing
columns → manual `ALTER TABLE`; Room `Migration`).

### 5. Key Flows — BEFORE / AFTER (ASCII)
The 1-3 important runtime paths (read path, write path, background job). Use box-drawing
`┌─┐ │ └─┘ → ▼`. Show branches, side-effects, where the new logic slots in. This is the centerpiece
that makes the change concrete — make it readable.

### 6. Worked Example (concrete numbers)
Walk ONE realistic scenario end-to-end with real-ish values (e.g. "user with 100 turns, asks X →
which block answers it"). Show the payload/context size stays bounded. Prove the design does what the
goal claims.

### 7. Module / File Map
Tree of files: `← NEW`, `← changed (what)`, `← unchanged`. Plus new dependencies/config. So the reader
sees the blast radius before any code.

### 8. Observability & Failure Modes
- Log lines to add (level by intent: error+exc → exception log, degraded → warning, milestone → info,
  diag → debug) and which sink they land in.
- Degradation: what happens when each new dependency/path fails (must the feature still work?).

### 9. Open Decisions / Risks
Anything needing the user's call, or a risk worth flagging (cost, RAM, latency, data growth). If none,
say so.

### 10. Handoff
One line: `Next: /breakdown-design <feature>` — and note that the implementation plan should land in
the **same** `{NN}-{Feature-Spec}/` folder as `{Feature-Spec}-implementation-plan.md`.

## N/A sections (be explicit, don't pad)
Android-only artifacts (screenshot/Visual Intent Map, Figma asset manifest, perf benchmarks,
Crashlytics capture chain) are **N/A** for non-Android stacks — write the one-line N/A reason instead
of inventing scope.

## Style
- **ASCII diagrams only.** No Mermaid, no images. Use `┌─┐ │ └─┘ → ▼ ◀ ✅ ⚠`.
- Match the sub-project's language convention for human-facing prose. Diagrams and labels: keep
  readable.
- Reference code as `path:line` so it's clickable.
- No char cap, but stay tight — design, not essay. If file mode, completeness > brevity.

## Coding Guidelines (workspace)
1. Define the data model before the flows. 2. Reuse existing tables/functions before adding new ones.
3. Split into modules; centralize state. 4. YAGNI — no dead components. 5. Double-check file paths are
real (you read them in Lookup). 6. Ask follow-up questions if the goal is unclear BEFORE designing.

## Avoid Repeating Mistakes
Read the nearest `CLAUDE.md` **Common Issues** before designing. If the design would touch a known
gotcha (e.g. a DB-session/locking pitfall, an auto-create that won't ALTER), bake the avoidance into
the design and call it out in §1 Constraints.
