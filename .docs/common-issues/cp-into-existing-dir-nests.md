# `cp -R src dst` nests inside dst when dst already exists

**Subject:** shell / file-ops · **Settled by:** observed `cp` behavior (deterministic).

## Rule
`cp -R src/ dst/` copies `src` *as* `dst` only when `dst` does **not** exist. If `dst` already
exists, `cp` puts `src` **inside** it → `dst/src/...` (a surprise nesting). In an agent workspace
the harness/IDE may have already created the target dir (e.g. a stub `.claude/settings.local.json`),
so "the dest doesn't exist yet" is not a safe assumption.

## What happened here
Copying another project's `.claude` into this workspace produced `workspace/.claude/.claude/...`
because the harness had pre-created `workspace/.claude/settings.local.json` first.

## How to apply
- To merge **contents** into an existing dir, copy the contents, not the dir:
  `cp -R src/. dst/` (note the trailing `/.`).
- Or check first: `[ -e dst ] && echo exists`.
- After any `cp -R`, run `ls dst` and confirm there's no accidental `dst/<srcname>/` nesting before
  moving on.
