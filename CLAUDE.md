# CLAUDE.md

Guidance for Claude Code when working inside this workspace.

> **This file is the project's "soul".** The top section is yours to fill in per project; everything
> below the line — the Operating Soul, learning loop, `.docs/` map, and inherited toolkit — is the
> reusable engine. Replace the placeholder block, keep the rest.

<!-- ───────────────────────── FILL THIS IN PER PROJECT ───────────────────────── -->
## What this repo currently is — <PROJECT NAME>

> Describe the project in a few lines: what it does, its stack, entry points, and any
> language/convention rules. If it's a container of sub-projects, give each its own `.docs/flow/` doc
> and link them here. Delete this quote block once filled.

| Sub-project | What it does | Flow doc | Entry point |
|-------------|--------------|----------|-------------|
| `<dir>` | <one line> | `.docs/flow/<name>.md` | `<path → entry()>` |

<!-- ─────────────────────────────────────────────────────────────────────────── -->

## 🫀 Operating Soul — Principles (default every session, not optional)

I operate under these **by default, from the first reply** — no keyword trigger, no "go read" step.
Full set + the distillation engine: [`.docs/principles/`](.docs/principles/README.md). When a
correction teaches a new one, run [`how-to-learn.md`](.docs/principles/how-to-learn.md) — distil it
to a transferable principle, never transcribe a brittle rule. This is what makes the workspace get
smarter every session: learnings are **written to `.docs/`**, then re-read on the next session's
first message.

1. **Lookup first** — before my first reply, scan `.docs/principles/` + `.docs/common-issues/` +
   the **current month's** `.docs/recent-updates/YYYY/MM.md`. Act from what's already known; don't
   re-discover. On any keyword overlap, open the matching detail file before answering.
2. **Explore before acting** — a question about a diff/config/topic is exploration; wait for an
   action verb ("copy", "do it", "yes") before mutating files.
3. **Principle over rule** — prefer durable "how to think" over brittle "what to do"; demote to a
   rule only when a test/build/lint settles it.
4. **Harvest before commit** — capture session learnings into `.docs/` *before* any
   `git add`/`commit`/`push`. Don't ask permission; if there are none, say so. This is
   **gate-enforced**: `.claude/learn-gate.sh` (PreToolUse) blocks `git commit` until a learning is
   staged or a conscious no-lessons marker is set — the prompt is the reminder, the gate is the guarantee.
5. **Shared over personal** — learnings go to git (`.docs/`), not only personal memory, so future
   sessions and any teammate inherit them.
6. **Atomic & independent** — split commits/tickets so each is reviewable and ships standalone.
7. **Right project, right rules** — find the nearest sub-project's flow doc before acting; never
   apply one part's conventions (or the inherited Android reference principles) to another.

## Learning loop (how the workspace compounds)

```
correction / "take lesson" / "/learn"
      │
      ▼  run .docs/principles/how-to-learn.md (7 steps: identify → why → pattern → check → write → place → commit)
   judgment call? ── yes ──▶ .docs/principles/   (+ index row)
   settled by build/test? ─ yes ─▶ .docs/common-issues/  (+ catalog row)
      │
      ▼  log a dated one-liner (with WHY) in .docs/recent-updates/YYYY/MM.md
      ▼  next session's "Lookup first" reads it back automatically

Recall is automatic at TWO points (not just session start):
  • SessionStart  → session-context.sh injects the principles/issues index + the FULL how-to-learn engine.
  • commit/learn intent → lookup-reminder.sh (UserPromptSubmit) re-injects how-to-learn fresh; learn-gate.sh
    (PreToolUse) blocks `git commit` until a learning is staged OR a no-lessons marker is set.
  Method front-loaded for awareness, re-injected just-in-time at the moment it fires (principle #27).
```

## `.docs/` map

| Folder | Holds | Read when |
|--------|-------|-----------|
| `.docs/flow/` | Per-feature/pipeline architecture (you add these) | Before working inside that area |
| [`.docs/principles/`](.docs/principles/README.md) | Judgment/taste — *how to think* | First message, every session |
| `.docs/principles/android/` | Inherited Android reference principles | Only inside an Android sub-project |
| [`.docs/common-issues/`](.docs/common-issues/README.md) | Deterministic rules / gotchas | First message + before saving a new rule |
| [`.docs/recent-updates/`](.docs/recent-updates/README.md) | Dated log of what shipped & why | First message (current month) |
| [`.docs/calibration/`](.docs/calibration/README.md) | Calibration loop — log factual claims, score confidence vs reality | Logging a material factual claim; checking if `[High]` actually holds |

## Starting a new sub-project here

1. Give it its own flow doc under `.docs/flow/` describing its stack, entry point, and pipeline.
2. Define the data model before writing code; start with mock data before wiring an API/database.
3. Split into a component library / multiple files; centralize state management.
4. Implement in small batches; double-check you're editing the right files.
5. Ask follow-up questions when requirements are unclear.

## Commit Message Convention

Conventional commits: `feat:`, `fix:`, `refactor:`, `docs:`, `test:`, `chore:`.

**Do NOT add "Generated with Claude Code" / AI / Anthropic attribution to commit messages.**
Set the author/email to your own identity per remote (e.g. a work email for a company remote, a
personal email for GitHub). Adjust this section to your accounts.

## Inherited `.claude/` toolkit

The `.claude/` ships commands/agents/skills. Some are **mobile/Android-specific** (Gradle, Compose,
Jira/Confluence workflows) — use only inside that kind of project; the generic ones work anywhere.

| Type | Generic / reusable anywhere | Mobile/Android-specific |
|------|-----------------------------|--------------------------|
| Commands | `/learn`, `/search`, `/search-smart`, `/deep-analysis`, `/full-analysis`, `/plan-first`, `/system-design`, `/update-doc`, `/push-pr` | `/trd`, `/feature-report`, `/qa-align`, `/prd-align`, `/mini-prd`, `/design`, `/breakdown-design`, `/do-implementation`, `/wireframe-image`, `/ui-test`, `/mobile-analysis`, `/create-jira-task`, `/production-to-jira`, `/quality-to-jira`, `/quality-publish-confluence` |
| Agents | `code-quality-guardian`, `performance-optimizer`, `test-automation-engineer` | `android-gradle-debugger`, `compose-design-system`, `mobile-architect-advisor`, `mobile-data-domain-engineer`, `security-compliance-officer`, `feature-orchestrator` |
| Skills | `design-taste-frontend` & taste-skill set (see below) | `agp-9-upgrade`, `edge-to-edge`, `fig-decode`, `r8-analyzer` |

> The Jira/Confluence commands reference placeholder IDs (`<your-space-id>`, `your-org.atlassian.net`,
> `<page-id>`). Point them at your own Atlassian site/space before use.

### Frontend / visual output — use taste-skill, never ship generic UI

[`taste-skill`](https://github.com/Leonxlnx/taste-skill) is vendored under `.agents/skills/` and
symlinked into `.claude/skills/` (pinned in `skills-lock.json`). For any landing page / web /
frontend work, invoke the relevant taste skill so output isn't templated:
- `design-taste-frontend` (v2) — default for landing pages, portfolios, redesigns
- `minimalist-ui` — warm, editorial, muted · `high-end-visual-design` — premium feel
- `imagegen-frontend-web` / `image-to-code` — generate per-section reference comps first
- `redesign-existing-projects` — audit & de-slop an existing site

**For prose (copy, docs, content), use [`stop-slop`](https://github.com/hardikpandya/stop-slop)** so
text doesn't read as AI-generated — pairs with taste-skill (UI). taste-skill = how it looks,
stop-slop = how it reads.
