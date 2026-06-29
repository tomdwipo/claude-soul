# Enforce a guardrail at the most UNIVERSAL layer that survives the consumer switching tools

**When this applies:** you're implementing a guardrail, capability, or convention that multiple
heterogeneous consumers depend on (different AI agents, editors, CI systems, humans) — and you must pick
*which layer* to implement it in. The tempting default is the layer you're already in (one tool's
proprietary extension point: a Claude Code `PreToolUse` hook, a Cursor rule, a bespoke plugin).

**Principle:** implement the enforcement at the **lowest common substrate** every consumer already passes
through — git (pre-commit hooks), the OS, the protocol, a plain file format — not in a single tool's
proprietary mechanism. A guardrail in tool X's extension point silently *disappears* the moment work
happens through tool Y. The universal layer survives consumer churn; the proprietary layer is a
single-vendor bet. Keep a *richer* tool-specific variant on top for UX, but the **floor must be portable**.

**Why:** we built a "harvest learnings before commit" gate as a Claude Code `PreToolUse` hook — perfect
*inside Claude Code*, invisible to Cursor/Gemini/Kiro/a human at the terminal. The same intent dropped to
a **git `pre-commit` hook** enforces it for *every* tool and even manual commits, because git runs it
regardless of who staged the change. Likewise the operating-soul instructions: a `CLAUDE.md` binds one
tool; an `AGENTS.md` (cross-tool convention) + symlinks bind them all. The portable layer is strictly
more reliable as the toolset changes — which it always does.

**How to apply:**
- Ask "what's the **narrowest layer all consumers share**?" — for repo-scoped enforcement that's almost
  always **git** (hooks) or a **plain file** (markdown/JSON), not an agent's hook API.
- Ship the portable floor first; add tool-specific richness (better messages, auto-injection) as an
  *enhancement on top*, never as the only copy.
- Detect the consumer and adapt the wiring (e.g. an installer that symlinks `AGENTS.md` to each tool's
  instruction file) rather than forcing one tool's convention on everyone.
- Pairs with [[intercept-deterministically-when-model-resists]] (the gate is still a deterministic
  intercept — just moved to a layer everyone shares) and [[inject-recall-upfront-method-just-in-time]].
