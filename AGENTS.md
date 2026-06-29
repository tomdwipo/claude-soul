# AGENTS.md — Operating Soul (tool-agnostic)

This is the **canonical** instruction file for any AI coding agent working in this repo. It is written
to the cross-tool [`AGENTS.md`](https://agents.md) convention so one file serves Claude Code, Cursor,
Gemini CLI, Kiro, Copilot, Windsurf, Cline, Aider, and anything else that reads a project instruction
file. Nothing here depends on a specific vendor's features — where automation helps it is noted, but the
**loop works by hand on any tool** (graceful degradation).

> **Point your tool at this file.** Most agents auto-load their own filename; make that file *be* or
> *point to* this one (symlink or one-line include) so there is a single source of truth:
>
> | Tool | File it loads | Wire-up |
> |------|---------------|---------|
> | Claude Code | `CLAUDE.md` | keep `CLAUDE.md`, or `ln -s AGENTS.md CLAUDE.md` |
> | Cursor | `.cursor/rules/*.mdc` | add a rule that says "follow `AGENTS.md`" |
> | Gemini CLI | `GEMINI.md` | `ln -s AGENTS.md GEMINI.md` |
> | Kiro | `.kiro/steering/*.md` | a steering file that includes `AGENTS.md` |
> | GitHub Copilot | `.github/copilot-instructions.md` | include/point to `AGENTS.md` |
> | Windsurf | `.windsurf/rules/` | a rule pointing to `AGENTS.md` |
> | Cline / Roo | `.clinerules` | `ln -s AGENTS.md .clinerules` |
> | Aider | `CONVENTIONS.md` | `ln -s AGENTS.md CONVENTIONS.md` |

---

## 🫀 Operating principles (default every session — not optional)

Act from these from the first reply; no trigger word needed. Full set + the engine that grows them:
[`.docs/principles/`](.docs/principles/README.md).

1. **Lookup first** — before the first reply, scan `.docs/principles/` + `.docs/common-issues/` + the
   current month's `.docs/recent-updates/YYYY/MM.md`. Act from what's already known; don't re-discover.
   On any keyword overlap, open the matching detail file before answering.
2. **Explore before acting** — a question about a diff/config/topic is exploration; wait for an action
   verb ("do it", "yes", "build it") before mutating files.
3. **Principle over rule** — prefer durable "how to think" over brittle "what to do"; demote to a rule
   only when a test/build/lint settles it.
4. **Harvest before commit** — capture session learnings into `.docs/` *before* any `git add`/`commit`.
   This is **gate-enforced** by `hooks/pre-commit` (see below). Don't ask permission; if there are none,
   opt out consciously (`SOUL_NO_LESSONS=1`).
5. **Shared over personal** — learnings go to git (`.docs/`), not a tool's private memory, so the next
   session *and any teammate on any tool* inherit them.
6. **Atomic & independent** — split commits so each is reviewable and ships standalone.
7. **Verify the live system** — docs can drift; for anything about real runtime state (flags, prod,
   infra) check the actual config/runtime, not the doc.

---

## The learning loop — why this repo gets smarter every session

```
            ┌──────────────────────── SESSION  N ────────────────────────┐
            │  work happens → a correction / gotcha / "take lesson"       │
            │        │                                                    │
            │        ▼  DISTIL  (run .docs/principles/how-to-learn.md)    │
            │        │  identify → why → generalises? → check existing →  │
            │        │  write → place → keep tight                        │
            │        ▼                                                    │
            │   judgment/taste ─→ .docs/principles/<name>.md  (+ index)   │
            │   settled by test ─→ .docs/common-issues/<name>.md (+ row)  │
            │        │                                                    │
            │        ▼  GATE:  hooks/pre-commit refuses the commit until  │
            │        │   a learning is staged (or you opt out on purpose) │
            │        ▼                                                    │
            │   committed → the knowledge base grows by ONE durable fact  │
            └────────────────────────────┬───────────────────────────────┘
                                          │  git push  (knowledge lives in
                                          │  version control, not in chat)
            ┌────────────────────────────▼─────────────── SESSION N+1 ───┐
            │  RECALL: the instruction file + (if supported) a session    │
            │  hook load .docs/ into context  →  the agent already KNOWS   │
            │  lesson N before the first reply                            │
            │        │                                                    │
            │        ▼  doesn't re-discover lesson N  →  spends effort on  │
            │           a NEW gotcha  →  distils lesson N+1  ──────────────┼──┐
            └─────────────────────────────────────────────────────────────┘  │
                          ▲                                                    │
                          └──────────────── the ratchet ──────────────────────┘
              every session starts from a strictly larger base than the last
```

**Why it actually compounds (not just "notes in a folder"):**

1. **Persistence beats memory.** A chat's context is ephemeral — it dies with the session. Writing the
   lesson to `.docs/` in **git** makes it survive sessions, machines, teammates, *and tool switches*.
2. **Recall is front-loaded, not hoped-for.** Next session the lesson is *in context before the first
   reply* (via the instruction file, and a SessionStart hook where the tool supports one). The agent
   can't "forget to check its notes" — they're already there.
3. **The gate stops silent loss.** Without enforcement, "I'll write it down later" loses most lessons.
   `hooks/pre-commit` forces the decision to be *recorded* (write it, or consciously skip) at the one
   moment every change passes through: the commit.
4. **Signal stays signal.** The principle-vs-rule split + "generalises to 3+ cases?" gate (in
   `how-to-learn.md`) keep the base from bloating into noise — so recall stays useful as it grows.

Net effect: nothing learned is lost, and everything learned is auto-recalled — a **monotonic ratchet**.
Each session can only start *at least as smart* as the last, usually smarter.

> **Honesty / limits.** The mechanics automate *recall* and *gate* the *capture* — they do **not** make
> the agent decide *whether* a correction is a real, generalisable lesson (that's judgment), nor do they
> *apply* a lesson for you (also judgment). The gate forces the question to be answered, not answered
> well. And docs drift — verify live state against the real system, not the doc.

---

## `.docs/` map

| Folder | Holds | Read when |
|--------|-------|-----------|
| [`.docs/principles/`](.docs/principles/README.md) | Judgment/taste — *how to think* | First message, every session |
| [`.docs/common-issues/`](.docs/common-issues/README.md) | Deterministic rules / gotchas | First message + before saving a new rule |
| [`.docs/recent-updates/`](.docs/recent-updates/README.md) | Dated log of what shipped & why | First message (current month) |
| `.docs/principles/how-to-learn.md` | The distillation engine (run on any correction) | When capturing a lesson |

---

## The harvest gate (tool-agnostic)

`hooks/pre-commit` is a **git-native** version of the capture gate — it works regardless of which AI tool
(or no tool) makes the commit, because git runs it. Activate once per clone:

```bash
git config core.hooksPath hooks      # point git at the tracked hooks/ dir
# or: cp hooks/pre-commit .git/hooks/pre-commit && chmod +x .git/hooks/pre-commit
```

It blocks a commit unless a learning is staged under `.docs/{principles,common-issues}`. No lesson this
commit? Opt out consciously: `SOUL_NO_LESSONS=1 git commit …`. (Claude Code users also get a richer
`PreToolUse` variant, `.claude/learn-gate.sh`, that injects the engine on block — but the git hook is the
portable floor.)

## Starting work here

1. Lookup first (principle 1). 2. Explore before mutating (principle 2). 3. When you learn something
durable, distil it with `how-to-learn.md` and stage it — the gate will remind you at commit time.
