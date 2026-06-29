#!/usr/bin/env bash
# claude-soul — SessionStart hook. Makes the learning loop actually AUTOMATIC: injects the
# lookup-first corpus (principles + common-issues catalog + c4 TOC if present) into context every
# session, so the agent recalls prior lessons without having to remember to scan. Pairs with the
# Operating Soul in CLAUDE.md. Emits INDEXES only (compact). Never fails the session (best-effort).
set -uo pipefail
D="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "$0")/.." 2>/dev/null && pwd)}/.docs"
[ -d "$D" ] || exit 0
y="$(date -u +%Y 2>/dev/null || echo '')"; m="$(date -u +%m 2>/dev/null || echo '')"

echo "════════ LOOKUP-FIRST CONTEXT (auto-injected by claude-soul; open the detail file on keyword match) ════════"

if [ -f "$D/principles/README.md" ]; then
  echo; echo "🫀 OPERATING SOUL / PRINCIPLES — how to think (judgment). Detail: .docs/principles/<name>.md"
  grep -E '^\| *[0-9]+ ' "$D/principles/README.md" 2>/dev/null || echo "  (principles index empty)"
fi

# The distillation METHOD in full (not just the index) — front-loaded so "how to turn a
# correction into a principle" is in context every session, ready at harvest time (usually the
# session END). Re-injected just-in-time on commit/learn intent by lookup-reminder.sh + learn-gate.sh.
if [ -f "$D/principles/how-to-learn.md" ]; then
  echo; echo "🧪 HOW TO LEARN (distillation engine — run on any correction / \"take lesson\" / /learn):"
  sed 's/^/  /' "$D/principles/how-to-learn.md"
fi

if [ -f "$D/common-issues/README.md" ]; then
  echo; echo "⚠️ COMMON ISSUES — deterministic gotchas, READ BEFORE coding/deploy. Detail: .docs/common-issues/<name>.md"
  grep -E '^\| ' "$D/common-issues/README.md" 2>/dev/null | grep -vE '^\| *(Kategori|Category|Subject|Area|---|:--)' || echo "  (catalog empty)"
fi

if [ -f "$D/c4/README.md" ]; then
  echo; echo "🏛️ ARCHITECTURE (as-built TOC). Detail: .docs/c4/NN-*.md"
  sed -nE '/Daftar Isi|Table of Contents|## TOC/,/Quick facts|^## [A-Z]/p' "$D/c4/README.md" 2>/dev/null | grep -E '^\| ' | grep -E '\]\([^)]+\)' || echo "  (c4 TOC empty)"
fi

if [ -n "$y" ] && [ -f "$D/recent-updates/$y/$m.md" ]; then
  echo; echo "📌 RECENT UPDATES this month: .docs/recent-updates/$y/$m.md — read it for what shipped + WHY."
fi

echo; echo "⚠️ DOCS CAN DRIFT — for anything about the LIVE system (flags, prod state, infra), VERIFY against the"
echo "   real config/runtime, do NOT trust the doc blindly (principle: validate in the real runtime context)."
echo "═══════════════════════════════════════════════════════════════════════════════════════════════════"
exit 0
