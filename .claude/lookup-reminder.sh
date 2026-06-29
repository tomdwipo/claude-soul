#!/usr/bin/env bash
# claude-soul — UserPromptSubmit hook. A LIGHT lookup-first nudge (~1-2 lines) on every prompt.
# The full lookup-first corpus is injected once by session-context.sh (SessionStart); re-dumping it
# per prompt would be wasteful and break prompt caching. This just keeps the discipline salient.
# Best-effort, never fails the turn.
set -uo pipefail

# stdin carries the UserPromptSubmit JSON ({prompt: "..."}); consume it once for the intent check.
IN="$(cat 2>/dev/null || true)"

y="$(date -u +%Y 2>/dev/null || echo '')"; m="$(date -u +%m 2>/dev/null || echo '')"
ru=""; [ -n "$y" ] && ru=" + .docs/recent-updates/$y/$m.md"
echo "🫀 Lookup-first: match your task keywords against .docs/principles/ + .docs/common-issues/ (open the detail file on a hit)${ru}. Harvest any new lesson into .docs/ (+ an index row) BEFORE committing. For claims about the LIVE system (flags, prod state, infra), verify against the real config/runtime — don't trust the doc blindly."

# Just-in-time distillation engine: re-inject the FULL how-to-learn fresh at the bottom of context
# exactly when the prompt signals a commit/learn moment — defeats the attention-dilution of the copy
# front-loaded at SessionStart. Fires only on intent (not every turn) → no per-turn bloat / cache churn.
D="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "$0")/.." 2>/dev/null && pwd)}/.docs"
HTL="$D/principles/how-to-learn.md"
PROMPT="$(printf '%s' "$IN" | jq -r '.prompt // empty' 2>/dev/null || true)"
[ -z "$PROMPT" ] && PROMPT="$IN"
if [ -f "$HTL" ] && printf '%s' "$PROMPT" \
     | grep -Eiq '(commit|git push|take lesson|/learn|harvest|distil)'; then
  echo
  echo "🧪 Commit/learn intent detected — distillation engine (fresh, anti-dilution):"
  echo "────────────────────────────────────────────────────────────"
  cat "$HTL"
  echo "────────────────────────────────────────────────────────────"
fi
