#!/usr/bin/env bash
# Stop hook — auto-capture calibration claims. When the assistant finishes a turn, scan the
# transcript for <!--CALIB {...}--> markers it emitted on material factual claims and log them to
# .docs/calibration/log.jsonl (dedup by content hash). The VERDICT stays manual — this only removes
# the manual `calib.py log` step; it does NOT make calibration autonomous.
#
# Best-effort by design: any failure exits 0 so a Stop hook can NEVER wedge or fail a turn.
set -u

ROOT="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "$0")/.." 2>/dev/null && pwd)}"
CALIB="$ROOT/.docs/calibration/calib.py"
[ -f "$CALIB" ] || exit 0

IN="$(cat 2>/dev/null || true)"
# Cheap pre-filter: skip the python spawn entirely on turns with no CALIB marker in the transcript.
case "$IN" in *transcript_path*) : ;; *) exit 0 ;; esac

TP="$(printf '%s' "$IN" | jq -r '.transcript_path // empty' 2>/dev/null || true)"
[ -n "$TP" ] && [ -f "$TP" ] || exit 0
grep -q 'CALIB' "$TP" 2>/dev/null || exit 0   # nothing to capture → don't spawn python

python3 "$CALIB" capture --transcript "$TP" >/dev/null 2>&1 || true
exit 0
