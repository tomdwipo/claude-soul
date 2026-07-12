# claude-soul

A self-improving **Operating Soul** for AI coding agents — drop a toolkit into any project with one
command and a `.docs/` knowledge base that gets smarter every session through a built-in learning loop.

> **Built for Claude Code first, portable to any agent.** The richest integration is Claude Code (a
> `CLAUDE.md` template + a `.claude/` command/agent/skill toolkit + lifecycle hooks). But the core — the
> Operating Soul, the learning loop, and the harvest gate — is just plain `AGENTS.md` + `.docs/` markdown
> + a git hook, so it works with **Cursor, Gemini CLI, Kiro, Copilot, Windsurf, Cline, Aider** too.
> Tool-specific features layer *on top* of a portable floor; nothing core is locked to one vendor.
> → [Works with any AI agent](#works-with-any-ai-agent-cursor-gemini-kiro-copilot-claude-code-).

## What makes it different

Most "memory" tools for coding agents store **rules** — facts and conventions to recall. claude-soul also
captures **how to think**, so each session the agent judges your intent better instead of just remembering
more rules. Three pieces do that:

- **Principle over rule.** If a test/build/lint can settle it, it's a *rule* (`.docs/common-issues/`). If
  it's judgment or taste, it's a *principle* (`.docs/principles/`). Corrections aren't forced into rigid
  rules, so the knowledge base doesn't overfit to one case.
- **7 levels of delegation** — Tell → Sell → Consult → Agree → Advise → Inquire → Delegate — measure how
  much interpretation you hand the agent. Default to *Tell* (the exact, explicit action); climb only once a
  consumer is proven reliable. ([detail](.docs/principles/delegation-level-match-consumer.md))
- **Learning loop.** Every lesson is distilled (`.docs/principles/how-to-learn.md`), stored in git, and
  auto-recalled next session — so the more you use it, the sharper its judgment about *your* codebase.

## Install

From **inside the project** you want to set up:

```bash
curl -fsSL https://raw.githubusercontent.com/tomdwipo/claude-soul/main/install.sh | bash
```

Prefer not to pipe to `bash`? Clone and run it (optionally pass a target dir):

```bash
git clone https://github.com/tomdwipo/claude-soul.git
./claude-soul/install.sh /path/to/your-project    # defaults to the current dir
```

Open the project in Claude Code — `CLAUDE.md` loads on the first message and the soul is active.

## Works with any AI agent (Cursor, Gemini, Kiro, Copilot, Claude Code, …)

The Operating Soul is a plain `AGENTS.md` (the [cross-tool convention](https://agents.md)) + a
`.docs/` knowledge base — nothing vendor-specific. One command auto-detects which agent(s) your repo
uses, points each one's instruction file at `AGENTS.md`, and activates the git-native harvest gate:

```bash
bash install-agents.sh        # detect → wire → activate; idempotent, never clobbers existing files
```

Prefer to wire it by hand? Each agent just needs its instruction file to point at `AGENTS.md`:

| Agent | Instruction file it reads | Wire-up |
|-------|---------------------------|---------|
| **Claude Code** | `CLAUDE.md` | keep `CLAUDE.md`, or `ln -s AGENTS.md CLAUDE.md` |
| **Cursor** | `.cursor/rules/*.mdc` | a rule file (`alwaysApply: true`) that says "follow `AGENTS.md`" |
| **Gemini CLI** | `GEMINI.md` | `ln -s AGENTS.md GEMINI.md` |
| **Kiro** | `.kiro/steering/*.md` | a steering file that includes `AGENTS.md` |
| **GitHub Copilot** | `.github/copilot-instructions.md` | point/include `AGENTS.md` |
| **Windsurf** | `.windsurf/rules/` | a rule pointing to `AGENTS.md` |
| **Cline / Roo** | `.clinerules` | `ln -s AGENTS.md .clinerules` |
| **Aider** | `CONVENTIONS.md` | `ln -s AGENTS.md CONVENTIONS.md` |

**The harvest gate is tool-agnostic.** Claude Code gets a rich `PreToolUse` variant (injects the engine
on block); every other tool — and a plain human at the terminal — is covered by `hooks/pre-commit`, which
**git** runs regardless of who commits. Activate it (done for you by `install-agents.sh`):

```bash
git config core.hooksPath hooks         # or: cp hooks/pre-commit .git/hooks/ && chmod +x .git/hooks/pre-commit
SOUL_NO_LESSONS=1 git commit …          # conscious opt-out when a commit genuinely has no lesson
```

> **Why a git hook, not just an agent hook?** A guardrail living in one tool's extension point vanishes
> the moment you work through another tool. Git is the layer *every* tool and every human shares — so the
> enforcement floor belongs there (see `.docs/principles/` → "enforce at the most universal layer").

## What lands in your project

```
AGENTS.md            ← tool-agnostic Operating Soul (canonical; works with ANY agent — see below)
CLAUDE.md            ← Operating Soul + learning loop (you fill in the "What this repo is" block)
install-agents.sh    ← auto-detect your AI agent(s) → wire AGENTS.md + activate the harvest gate
hooks/pre-commit     ← git-native harvest gate (tool-agnostic floor; works even without any AI tool)
.claude/
  ├─ commands/          ← slash commands (/learn, /plan-first, /search, /push-pr, …)
  ├─ agents/            ← specialized subagents
  ├─ skills/            ← symlinks into ↓
  ├─ settings.json      ← wires three hooks: SessionStart + UserPromptSubmit + PreToolUse
  ├─ session-context.sh ← SessionStart: injects principles + common-issues + c4 TOC + the how-to-learn engine
  ├─ lookup-reminder.sh ← UserPromptSubmit: per-turn lookup nudge + just-in-time how-to-learn on commit/learn intent
  ├─ learn-gate.sh      ← PreToolUse(Bash): blocks `git commit` until a learning is staged or a no-lessons marker is set
  └─ learn-hooks-eval.sh← repeatable eval for the two hooks above (run after changing them)
.agents/skills/      ← vendored skill sources (taste-skill, stop-slop, …)
.docs/
  ├─ principles/     ← how-to-think + the how-to-learn distillation engine
  ├─ common-issues/  ← deterministic gotchas
  └─ recent-updates/ ← dated learning log
skills-lock.json     ← pins the vendored skills
```

## Semantic code search (`tools/code-rag`)

An optional local **MCP tool** the installer drops in: semantic **+** keyword search over *your*
repository — source code **and** docs — exposed to any agent as `search_code`. Runs fully local
(no code leaves your machine), natural-language queries in any language, returns `path:line`.

- **Embedding** `qwen3-embedding:0.6b` on host **Ollama** (GPU/Metal), **vector DB** Qdrant (Docker).
- **Retrieval** hybrid dense + BM25 (RRF) → `bge-reranker-v2-m3` int8 cross-encoder, then a
  `RERANK_MIN_SCORE` cutoff — so an off-topic query returns *nothing* instead of noise.
- **Auto-index + prune** — a watcher re-embeds only changed chunks and drops stale/deleted ones, so
  the index tracks the working tree (edits, branch switches) with no manual rebuild.
- Both models are deliberately **general** (code + prose + multilingual), not code-only — a repo is
  code *and* docs, and queries aren't always English. Swap via `EMBED_MODEL` / `RERANKER_MODEL`.

```bash
cd tools/code-rag && make up      # needs Docker (≥8 GB) + Ollama; then add the .mcp.json entry
```

When it's connected, the Operating Soul grounds answers/`/plan-first`/`/breakdown-design` through it
before falling back to grep. Full guide, multi-checkout mode, and the "why these models" rationale:
**[`tools/code-rag/README.md`](tools/code-rag/README.md)**.

## Safe to re-run

The installer **merges**, it does not stomp:

- **Shared toolkit** (`.claude/{commands,agents,skills}`, `.agents/`) is refreshed wholesale — that's the engine.
- **`.docs/`** is *seeded*: missing baseline files are added, your own evolved docs are kept.
- **`CLAUDE.md`** is never overwritten — if one exists, the template lands as `CLAUDE.soul.md`.
- **`.claude/settings.local.json`** and **`.docs/flow/`** are never touched.
- **`.gitignore`** gets a one-time block that keeps the toolkit tracked while ignoring local/runtime/secret files.

## The learning loop — why it gets smarter every session

```
        ┌───────────────────────── SESSION N ─────────────────────────┐
        │  correction / gotcha / "take lesson"                         │
        │       │                                                      │
        │       ▼  DISTIL  → .docs/principles/how-to-learn.md          │
        │       │   (identify → why → generalises? → write → place)    │
        │       ▼                                                      │
        │   judgment ─→ .docs/principles/   |   test-settled ─→ .docs/common-issues/
        │       │                                                      │
        │       ▼  GATE  → pre-commit refuses the commit until the     │
        │       │   lesson is written (or you consciously opt out)     │
        │       ▼                                                      │
        │   committed → knowledge base grows by ONE durable fact       │
        └───────────────────────────┬──────────────────────────────────┘
                                     │  git push — knowledge lives in version
                                     │  control, NOT in disposable chat context
        ┌────────────────────────────▼──────────────── SESSION N+1 ────┐
        │  RECALL → instruction file (+ session hook) loads .docs/      │
        │  into context: the agent ALREADY KNOWS lesson N before its    │
        │  first reply → doesn't re-discover → spends effort on a NEW   │
        │  gotcha → distils lesson N+1 ─────────────────────────────────┼──┐
        └───────────────────────────────────────────────────────────────┘  │
                       ▲                                                     │
                       └───────────────── the ratchet ──────────────────────┘
            every session starts from a strictly larger base than the last
```

**Why this actually compounds (vs. just "notes in a folder"):**

1. **Persistence beats memory** — a chat context dies with the session; a lesson written to `.docs/` in
   **git** survives sessions, machines, teammates, *and tool switches*.
2. **Recall is front-loaded, not hoped-for** — next session the lesson is in context *before the first
   reply*; the agent can't "forget to check its notes."
3. **The gate stops silent loss** — "I'll write it later" loses most lessons; the commit chokepoint forces
   the decision to be *recorded*.
4. **Signal stays signal** — the principle-vs-rule split + the "generalises to 3+ cases?" gate keep the
   base from bloating into noise as it grows.

Net effect: nothing learned is lost, everything learned is auto-recalled → a **monotonic ratchet**. Each
session can only start *at least as smart* as the last.

---

## The learning loop (mechanics)

**Capture** — a correction or `/learn` runs `.docs/principles/how-to-learn.md` (identify → why →
pattern → check → write → place → commit). Judgment calls become **principles**; build/test-settled
facts become **common-issues**; a dated one-liner lands in **recent-updates**. Capture is now
**gate-enforced**: `learn-gate.sh` (PreToolUse) blocks `git commit` until a learning is staged under
`.docs/{principles,common-issues}` **or** a conscious per-session no-lessons marker is set — so the
discipline can't silently lapse when you're busy.

**Recall (automatic, at two points)** — `session-context.sh` (SessionStart) injects the **principles
index + common-issues catalog + architecture TOC + the full how-to-learn engine** at the start of *every*
session; and `lookup-reminder.sh` (UserPromptSubmit) re-injects `how-to-learn` **fresh** whenever a prompt
signals commit/learn intent — front-loaded for awareness, re-injected just-in-time at the moment it fires,
so the method lands at full attention even in a long session. Recall no longer depends on the agent
remembering to scan — the prior lessons are simply *there*, and the workspace compounds instead of
re-discovering. (Honesty: the hooks automate recall and now *gate* capture, but deciding *whether* a
correction is a real, generalizable lesson is still judgment — the gate forces the decision to be recorded,
it doesn't make it for you; and *applying* a lesson is judgment too. The hooks also remind that docs can
drift, so verify against the live system, not the doc, for anything about real runtime state.)

## Notes

- **Mobile/Android-specific** commands, agents, and skills are included but flagged in `CLAUDE.md`;
  use them only inside that kind of project. The Jira/Confluence commands carry **placeholder** IDs
  (`<your-space-id>`, `your-org.atlassian.net`) — point them at your own Atlassian site before use.
- **Symlinks:** the `.claude/skills/*` entries are git symlinks into `.agents/skills/`. macOS/Linux
  work out of the box; on Windows enable `git config core.symlinks true`.
- No secrets, tokens, or organization-internal content are bundled.

## License

MIT
