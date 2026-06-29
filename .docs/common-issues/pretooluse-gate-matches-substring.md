# A PreToolUse(Bash) gate keyed on a command substring fires on ANY Bash call containing that text

**Subject:** hooks / claude-soul · **Settled by:** observed hook behavior (the install-test was blocked by itself)

## The gotcha

`learn-gate.sh` (the harvest gate) blocks `git commit` by matching the substring `git commit` in the
PreToolUse Bash payload. That payload is the **whole command string** the agent is about to run — so the
gate also fires when a command merely *mentions* `git commit` without committing:

- a test harness that pipes `'{"...command":"git commit -m x"}'` into the gate (this is how we first saw it — the install test blocked itself),
- a `grep "git commit" …`, an `echo "how to git commit"`, docs tooling that prints the phrase.

This is inherent to substring interception: the shell can't parse intent, only presence.

## What to do

- **Escape per call:** set the conscious no-lessons marker — `touch "${TMPDIR:-/tmp}/claude-learn-nolessons-<session_id>"` — then re-run.
- **Better, during a real harvest session:** **stage a learning file first** (`git add .docs/principles/… ` or `.docs/common-issues/…`). That satisfies the gate's evidence-(a) check (`git diff --cached`), so every subsequent `git commit`-containing Bash call this session passes. You were going to stage the learning anyway.
- The second `case "$CMD"` check (parse `.tool_input.command` via `jq`, re-confirm it contains `git commit`) already filters the case where `git commit` sits only in a *non-command* JSON field — so noise is limited to commands whose actual text contains the phrase.

## Why not "fix" it to be exact?

Perfect shell-command parsing (is this *really* invoking `git commit`?) is unreliable and not worth it: the
marker + staged-evidence escapes make the false-positive harmless, and the gate must stay **best-effort,
fall-through-to-allow** so it never wedges committing. Keep it loose + documented over clever + brittle.

## Verify

Run `.claude/learn-hooks-eval.sh` — case **G5** pins that `git commit` in a non-command field is ignored,
**G1** pins the real block, **G3/G4** pin the two escapes. Feed real hook JSON through the script; don't assert.
