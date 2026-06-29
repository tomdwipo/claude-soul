# zsh does NOT word-split an unquoted scalar — `for f in $LIST` iterates ONCE over the whole string

**Subject:** shell / zsh · **Settled by:** observed loop behavior (deterministic; this session's shell is zsh).

## The gotcha

In **bash**, `LIST="a b c"; for f in $LIST` iterates 3 times (unquoted expansion is word-split on `$IFS`).
In **zsh** (the default shell here), the same code iterates **once** with `f="a b c"` — zsh does **not**
word-split unquoted parameters by default. So a loop / command built to fan out over a space-separated
variable silently collapses to a single giant argument.

Symptom seen: `for f in $NEW; do grep ... "$f.md"; done` → `grep: <entire list>.md: File name too long`
(the whole list got `.md` appended and passed as one filename), and existence checks that looked like they
"passed" actually never ran per-item.

## What to do

- **Run the snippet under bash explicitly** when it relies on word-splitting:
  `bash -c '... for f in $LIST; do ...; done'` (most reliable for one-off Bash-tool commands here).
- **Or split explicitly in zsh:** `for f in ${=LIST}` (the `=` flag forces field-splitting), or
  `for f in ${(s: :)LIST}` (split on a chosen separator), or make it a real array: `LIST=(a b c)`.
- **Quote when you DON'T want splitting** — that part zsh and bash agree on.

## Why it's easy to miss

The loop doesn't error loudly — it just runs once. A trailing `|| echo "all ok"` or `2>/dev/null` can
make a collapsed/failed loop *look* like a clean pass (see also: a guard that suppresses stderr can't tell
"no matches" from "command failed"). Verify the loop actually iterated (print a per-item line) before
trusting its summary.
