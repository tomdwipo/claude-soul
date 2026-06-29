#!/usr/bin/env bash
# claude-soul — learn-hooks-eval.sh — repeatable eval for the harvest-learning hooks
# (principle: eval-engineering — measure on the REAL path, don't just assert). Exercises:
#   • learn-gate.sh (PreToolUse) — in a HERMETIC temp git repo so the block path is
#     deterministic regardless of the host repo's staged state.
#   • lookup-reminder.sh (UserPromptSubmit, just-in-time how-to-learn) — through the real entrypoint.
# Prints a PASS/FAIL matrix; exits non-zero if any case fails. Read-only on the host repo.
set -u
HERE="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
PASS=0; FAIL=0
ok(){ printf "  ✅ %s\n" "$1"; PASS=$((PASS+1)); }
no(){ printf "  ❌ %s — %s\n" "$1" "$2"; FAIL=$((FAIL+1)); }

# ── Hermetic temp repo for the gate ───────────────────────────────────────────
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
mkdir -p "$TMP/.claude" "$TMP/.docs/principles" "$TMP/.docs/common-issues"
cp "$HERE/learn-gate.sh" "$TMP/.claude/learn-gate.sh"
cp "$HERE/../.docs/principles/how-to-learn.md" "$TMP/.docs/principles/how-to-learn.md"
( cd "$TMP" && git init -q && git config user.email e@e.co && git config user.name e \
  && git add -A && git commit -qm base )
# The gate resolves ROOT from $CLAUDE_PROJECT_DIR first; point it at the temp repo per-case.
GATE="$TMP/.claude/learn-gate.sh"
run_gate(){ printf '%s' "$2" | CLAUDE_PROJECT_DIR="$TMP" bash "$GATE" 1>/dev/null 2>"$TMP/err"; echo $?; }

echo "── learn-gate.sh (PreToolUse) ──────────────────────────────"

rc=$(run_gate sid1 '{"session_id":"sid1","tool_input":{"command":"git commit -m x"}}')
{ [ "$rc" = 2 ] && grep -q "HARVEST GATE" "$TMP/err" && grep -q "How to Learn" "$TMP/err"; } \
  && ok "G1 clean commit blocked + method injected" || no "G1" "rc=$rc"

rc=$(run_gate sid2 '{"session_id":"sid2","tool_input":{"command":"ls -la"}}')
{ [ "$rc" = 0 ] && [ ! -s "$TMP/err" ]; } && ok "G2 non-commit passes silently" || no "G2" "rc=$rc"

M="${TMPDIR:-/tmp}/claude-learn-nolessons-sid3"; touch "$M"
rc=$(run_gate sid3 '{"session_id":"sid3","tool_input":{"command":"git commit -m x"}}')
[ "$rc" = 0 ] && ok "G3 no-lessons marker allows" || no "G3" "rc=$rc"; rm -f "$M"

( cd "$TMP" && echo n > .docs/common-issues/x.md && git add .docs/common-issues/x.md )
rc=$(run_gate sid4 '{"session_id":"sid4","tool_input":{"command":"git commit -m x"}}')
[ "$rc" = 0 ] && ok "G4 staged learning allows" || no "G4" "rc=$rc"
( cd "$TMP" && git reset -q HEAD .docs/common-issues/x.md && rm -f .docs/common-issues/x.md )

rc=$(run_gate sid5 '{"session_id":"sid5","tool_input":{"command":"ls"},"note":"git commit"}')
[ "$rc" = 0 ] && ok "G5 commit-text outside command field ignored" || no "G5" "rc=$rc"

echo ""
echo "── lookup-reminder.sh (UserPromptSubmit) ───────────────────"
dumps(){ printf '%s' "$1" | bash "$HERE/lookup-reminder.sh" 2>/dev/null | grep -c "How to Learn"; }
for p in '{"prompt":"ok commit all and push"}' '{"prompt":"/learn this"}' \
         '{"prompt":"please take lesson from this"}' '{"prompt":"git push origin main"}' \
         '{"prompt":"harvest the learnings"}'; do
  [ "$(dumps "$p")" = 1 ] && ok "intent → method injected: $p" || no "intent: $p" "no dump"
done
for p in '{"prompt":"explain this function"}' '{"prompt":"refactor the mapper"}'; do
  [ "$(dumps "$p")" = 0 ] && ok "no-intent → stays light: $p" || no "no-intent: $p" "dumped"
done
printf '%s' '{"prompt":"hi"}' | bash "$HERE/lookup-reminder.sh" 2>/dev/null \
  | grep -q "Lookup-first" && ok "base nudge always emitted" || no "base nudge" "missing"

echo ""
echo "════════════════════════════════════════════"
echo "  RESULT: $PASS passed, $FAIL failed"
echo "════════════════════════════════════════════"
[ "$FAIL" = 0 ]
