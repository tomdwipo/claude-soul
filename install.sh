#!/usr/bin/env bash
#
# claude-soul installer — drop the Operating Soul toolkit into any project.
#
#   From inside your project:
#     curl -fsSL https://raw.githubusercontent.com/tomdwipo/claude-soul/main/install.sh | bash
#
#   Or from a clone:
#     ./install.sh [TARGET_DIR]      # defaults to the current directory
#
# Safe to re-run. It refreshes the shared toolkit, seeds the .docs/ knowledge base
# without overwriting your own edits, and never touches your CLAUDE.md,
# .claude/settings.local.json, or .docs/flow/.

set -euo pipefail

REPO_URL="https://github.com/tomdwipo/claude-soul.git"

say()  { printf '  %s\n' "$*"; }
head() { printf '\n→ %s\n' "$*"; }

# ── Resolve the source: a local clone if we're running from one, else fetch it ──
SELF="${BASH_SOURCE[0]:-}"
SRC=""; TMP=""
if [ -n "$SELF" ]; then
  D="$(cd "$(dirname "$SELF")" >/dev/null 2>&1 && pwd)"
  [ -f "$D/.claude-soul" ] && SRC="$D"
fi
if [ -z "$SRC" ]; then
  head "fetching claude-soul"
  TMP="$(mktemp -d)"
  git clone --depth 1 "$REPO_URL" "$TMP" >/dev/null 2>&1
  SRC="$TMP"
fi
cleanup() { [ -n "$TMP" ] && rm -rf "$TMP"; }
trap cleanup EXIT

# ── Resolve the target ──
TARGET="${1:-$PWD}"
TARGET="$(cd "$TARGET" >/dev/null 2>&1 && pwd)" || { echo "target dir not found: ${1:-$PWD}" >&2; exit 1; }

if [ -f "$TARGET/.claude-soul" ]; then
  echo "Refusing to install the soul into the soul repo itself." >&2
  exit 1
fi

head "installing soul into: $TARGET"
mkdir -p "$TARGET/.claude" "$TARGET/.docs"

# ── 1. Shared toolkit — MERGED, never deletes your extras (refresh engine files, keep project-only) ──
#    Copy the source dir's CONTENTS into the target ("$SRC/.../." form): same-named engine files are
#    refreshed, NEW ones added, and your project-only files (e.g. a custom command/skill the soul
#    doesn't ship) are preserved. The trailing "/." also dodges the cp-into-existing-dir nesting trap.
for d in agents commands skills; do
  mkdir -p "$TARGET/.claude/$d"
  cp -R "$SRC/.claude/$d/." "$TARGET/.claude/$d/"
done
mkdir -p "$TARGET/.agents"
cp -R "$SRC/.agents/." "$TARGET/.agents/"   # symlink targets for .claude/skills/*
cp "$SRC/skills-lock.json" "$TARGET/"
# All hook scripts settings.json wires (SessionStart / UserPromptSubmit / PreToolUse / Stop) MUST ship,
# else the referenced command is missing and the hook errors on every matching tool call. The eval
# harness ships too so installs can self-verify the gate on the real path (principle: eval-engineering).
for s in session-context.sh lookup-reminder.sh learn-gate.sh learn-hooks-eval.sh calib-capture.sh; do
  cp "$SRC/.claude/$s" "$TARGET/.claude/" && chmod +x "$TARGET/.claude/$s"
done
say "toolkit: commands, agents, skills (+ vendored skill sources) + recall/harvest hooks (session-context, lookup-reminder, learn-gate) + eval merged (your project-only files kept)"

# ── 1a2. Git-native harvest gate — the portable floor (works for any tool / plain git, not just Claude
#    Code's PreToolUse). The repo ships hooks/, but they only enforce anything once git is pointed at them.
if [ -d "$SRC/hooks" ]; then
  rm -rf "$TARGET/hooks"; cp -R "$SRC/hooks" "$TARGET/"; chmod +x "$TARGET/hooks/"* 2>/dev/null || true
  if ( cd "$TARGET" && git rev-parse --git-dir >/dev/null 2>&1 ); then
    ( cd "$TARGET" && git config core.hooksPath hooks )
    say "git-native gate: hooks/ copied + core.hooksPath=hooks wired"
  else
    say "git-native gate: hooks/ copied (not wired — target isn't a git repo; run 'git config core.hooksPath hooks' after 'git init')"
  fi
fi

# ── 1b. SessionStart hook — makes the learning loop AUTOMATIC; seed if missing, never clobber yours ──
if [ -e "$TARGET/.claude/settings.json" ]; then
  cp "$SRC/.claude/settings.json" "$TARGET/.claude/settings.soul.json"
  say ".claude/settings.json exists → hook written to settings.soul.json (merge the hooks block by hand)"
else
  cp "$SRC/.claude/settings.json" "$TARGET/.claude/settings.json"
  say ".claude/settings.json created → SessionStart auto-recall hook active"
fi

# ── 2. Knowledge base — seed missing files, never overwrite your evolved docs ──
for d in principles common-issues recent-updates calibration; do
  mkdir -p "$TARGET/.docs/$d"
  cp -Rn "$SRC/.docs/$d/." "$TARGET/.docs/$d/" 2>/dev/null || true
done
say ".docs: principles, common-issues, recent-updates, calibration seeded (existing files kept)"

# ── 3. CLAUDE.md — never clobber an existing one ──
if [ -e "$TARGET/CLAUDE.md" ]; then
  cp "$SRC/CLAUDE.md" "$TARGET/CLAUDE.soul.md"
  say "CLAUDE.md exists → soul template written to CLAUDE.soul.md (merge by hand)"
else
  cp "$SRC/CLAUDE.md" "$TARGET/CLAUDE.md"
  say "CLAUDE.md created → fill in the 'What this repo is' block"
fi

# ── 4. .gitignore — append the keep-toolkit / ignore-secrets block once ──
GI="$TARGET/.gitignore"
if ! grep -q 'claude-soul:ignore' "$GI" 2>/dev/null; then
  cat >> "$GI" <<'EOF'

# === claude-soul:ignore — local/runtime/personal (shared toolkit stays tracked) ===
.claude/settings.local.json
.claude/scheduled_tasks.lock
.claude/inbox/
.claude/outbox/
.claude/worktrees/
.claude/memory/
.mcp.json
EOF
  say ".gitignore: added local/runtime/secret ignores"
else
  say ".gitignore: already configured"
fi

# ── 5. code-rag — local semantic code+docs search (MCP). Copy the tool, then guide setup. ──
#    We COPY the tool (so it's present) + check prereqs, but never auto-`make up` from an installer
#    (it pulls multi-GB models + needs Docker running — that's an explicit, interactive step).
if [ -d "$SRC/tools/code-rag" ]; then
  mkdir -p "$TARGET/tools/code-rag"
  cp -R "$SRC/tools/code-rag/." "$TARGET/tools/code-rag/"
  rm -rf "$TARGET/tools/code-rag/.venv" "$TARGET/tools/code-rag"/**/__pycache__ 2>/dev/null || true
  say "code-rag: tools/code-rag/ installed (semantic code search MCP)"
  MISSING=""
  command -v docker >/dev/null 2>&1 || MISSING="$MISSING docker"
  command -v ollama >/dev/null 2>&1 || MISSING="$MISSING ollama"
  if [ -z "$MISSING" ]; then
    say "code-rag: Docker + Ollama found → finish setup with:  cd tools/code-rag && make up"
  else
    say "code-rag: install prereqs first —$MISSING (Docker: https://docker.com  ·  Ollama: https://ollama.com), then: cd tools/code-rag && make up"
  fi
  say "code-rag: then add the 'code-rag' entry from .mcp.json.example to your .mcp.json and restart the agent"
fi

printf '\n✓ Soul installed. Open the project in Claude Code and it loads on the first message.\n'
printf '  The harvest gate fires on commit (Claude Code PreToolUse + git-native pre-commit).\n'
printf '  code-rag semantic search: cd tools/code-rag && make up (needs Docker + Ollama).\n'
printf '  Next: edit CLAUDE.md, then commit .claude/ .agents/ hooks/ .docs/ tools/ CLAUDE.md\n\n'
