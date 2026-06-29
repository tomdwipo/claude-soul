#!/usr/bin/env bash
# claude-soul — learn-gate.sh — PreToolUse(Bash) harvest gate + just-in-time how-to-learn.
#
# Closes the Capture side of the loop: the model reliably SKIPS "harvest learnings before commit"
# when busy (a discipline its prior under-weights). A prompt nudge alone is a coin-flip, so this
# intercepts DETERMINISTICALLY (principle: intercept-deterministically-when-model-resists).
#
# It BLOCKS `git commit` (exit 2 → stderr fed back to the agent) until there is EVIDENCE the harvest
# question was answered this session — either a learning file is staged (.docs/principles or
# .docs/common-issues), OR an explicit per-session "no-lessons" marker exists. On block it injects
# the full how-to-learn engine (fresh = full attention; principle: inject-recall-upfront-method-jit).
#
# The shell never decides WHETHER there is a lesson (that stays LLM reasoning) — it only forces the
# decision to be RECORDED before a commit lands. Pairs with the Opsi-1 nudge in lookup-reminder.sh.
# Best-effort: any failure falls through to ALLOW — a gate must never wedge committing.
set -u

ROOT="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "$0")/.." 2>/dev/null && pwd)}"
[ -n "$ROOT" ] || exit 0
HTL="$ROOT/.docs/principles/how-to-learn.md"

IN="$(cat 2>/dev/null || true)"

# Fast path: only commits matter. Cheap raw substring check before parsing JSON, so the hook is
# ~free on the 99% of Bash calls that aren't commits.
case "$IN" in *"git commit"*) : ;; *) exit 0 ;; esac

CMD="$(printf '%s' "$IN" | jq -r '.tool_input.command // empty' 2>/dev/null || true)"
SID="$(printf '%s' "$IN" | jq -r '.session_id // empty' 2>/dev/null || true)"

# Confirm it's really a commit command, not "git commit" buried in another field.
case "$CMD" in *"git commit"*) : ;; *) exit 0 ;; esac

# Evidence (a): a learning file is staged in THIS commit → harvested → allow.
if (cd "$ROOT" && git diff --cached --name-only 2>/dev/null) \
     | grep -Eq '^\.docs/(principles|common-issues)/'; then
  exit 0
fi

# Evidence (b): explicit, conscious "no lessons this session" marker → allow.
MARK="${TMPDIR:-/tmp}/claude-learn-nolessons-${SID:-nosid}"
[ -f "$MARK" ] && exit 0

# Otherwise: BLOCK + surface the method fresh.
{
  echo "🛑 HARVEST GATE — commit blocked: no evidence a harvest decision was made this session."
  echo ""
  echo "Pick ONE, then commit again:"
  echo "  • There IS a lesson → run /learn → stage a file under .docs/principles or"
  echo "                        .docs/common-issues (git add) → commit again."
  echo "  • There is NONE     → record it consciously:  touch \"$MARK\"  → commit again."
  echo ""
  echo "── how-to-learn (distillation engine) ─────────────────────"
  [ -f "$HTL" ] && cat "$HTL"
  echo "───────────────────────────────────────────────────────────"
} >&2
exit 2
