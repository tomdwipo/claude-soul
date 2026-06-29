#!/usr/bin/env bash
# claude-soul — install-agents.sh
# Auto-detects which AI coding agent(s) this repo uses and wires each one's instruction file to the
# canonical AGENTS.md, then activates the git-native harvest gate. Idempotent and NON-DESTRUCTIVE:
# it symlinks/creates a pointer only when the target is absent; if a file already exists it just tells
# you the one line to add. Run from anywhere inside the repo:  bash install-agents.sh
set -u
ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$ROOT" || { echo "not in a repo"; exit 1; }
[ -f AGENTS.md ] || { echo "✗ AGENTS.md not found at repo root ($ROOT). Run from the claude-soul'd repo."; exit 1; }

LINKED=0; NOTED=0; DETECTED=0

# symlink a TOP-LEVEL instruction file → AGENTS.md (same dir, so target is just "AGENTS.md")
link_top(){
  local f="$1"
  if [ -e "$f" ] || [ -L "$f" ]; then
    echo "  • $f already exists — add this line near the top:   > Follow ./AGENTS.md"
    NOTED=$((NOTED+1))
  else
    ln -s AGENTS.md "$f" && { echo "  ✓ $f → AGENTS.md (symlink)"; LINKED=$((LINKED+1)); }
  fi
}
# write a NESTED pointer file (rule/steering dirs) that includes AGENTS.md via a relative path
pointer(){
  local f="$1" rel="$2" front="${3:-}"
  if [ -e "$f" ]; then
    echo "  • $f already exists — ensure it points to $rel"
    NOTED=$((NOTED+1))
  else
    mkdir -p "$(dirname "$f")"
    { [ -n "$front" ] && printf '%s\n' "$front"; \
      printf '# Operating Soul\n\nThis project follows the canonical operating soul. Read and obey [`%s`](%s).\n' "$rel" "$rel"; \
    } > "$f" && { echo "  ✓ $f → $rel (pointer)"; LINKED=$((LINKED+1)); }
  fi
}
seen(){ DETECTED=$((DETECTED+1)); echo "▶ detected: $1"; }

echo "Wiring AGENTS.md into detected agents…"

# ── Claude Code ──
if [ -d .claude ] || [ -f CLAUDE.md ]; then seen "Claude Code"; link_top CLAUDE.md; fi
# ── Cursor ──
if [ -d .cursor ] || [ -f .cursorrules ]; then seen "Cursor";
  pointer ".cursor/rules/soul.mdc" "../../AGENTS.md" $'---\nalwaysApply: true\n---'; fi
# ── Gemini CLI ──
if [ -d .gemini ] || [ -f GEMINI.md ]; then seen "Gemini CLI"; link_top GEMINI.md; fi
# ── Kiro ──
if [ -d .kiro ]; then seen "Kiro"; pointer ".kiro/steering/soul.md" "../../AGENTS.md"; fi
# ── GitHub Copilot ──
if [ -d .github ]; then seen "GitHub Copilot"; pointer ".github/copilot-instructions.md" "../AGENTS.md"; fi
# ── Windsurf ──
if [ -d .windsurf ] || [ -f .windsurfrules ]; then seen "Windsurf"; pointer ".windsurf/rules/soul.md" "../../AGENTS.md"; fi
# ── Cline / Roo ──
if [ -f .clinerules ] || [ -d .clinerules ]; then seen "Cline/Roo"; link_top .clinerules; fi
# ── Aider ──
if [ -f CONVENTIONS.md ] || ls .aider* >/dev/null 2>&1; then seen "Aider"; link_top CONVENTIONS.md; fi

if [ "$DETECTED" = 0 ]; then
  echo "  (no agent config detected — AGENTS.md alone works on any tool that reads a project"
  echo "   instruction file. To wire one explicitly, see the table in AGENTS.md.)"
fi

# ── Activate the git-native harvest gate (works for every tool + manual commits) ──
echo ""
echo "Activating the harvest gate (git pre-commit)…"
if [ -f hooks/pre-commit ]; then
  if [ -e .git/hooks/pre-commit ]; then
    echo "  • .git/hooks/pre-commit already exists — to use claude-soul's gate either replace it,"
    echo "    or run:  git config core.hooksPath hooks   (keeps it in sync with the tracked hooks/)"
  else
    cp hooks/pre-commit .git/hooks/pre-commit && chmod +x .git/hooks/pre-commit \
      && echo "  ✓ copied hooks/pre-commit → .git/hooks/pre-commit"
    echo "    (alternative, auto-syncing:  git config core.hooksPath hooks)"
  fi
else
  echo "  • hooks/pre-commit not found — skipping."
fi

echo ""
echo "Done: $DETECTED agent(s) detected, $LINKED file(s) wired, $NOTED need a manual one-liner."
echo "Skip the gate for a genuinely lesson-free commit with:  SOUL_NO_LESSONS=1 git commit …"
