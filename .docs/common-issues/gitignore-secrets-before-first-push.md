# Gitignore secret-bearing files BEFORE the first commit

**Subject:** git / security · **Settled by:** a leaked token is unrecoverable once pushed.

## Rule
Before `git init` → first `commit` → `push`, scan the working tree for files that carry live
secrets and add them to `.gitignore` **first**. A secret pushed to a remote (even a private repo)
must be treated as compromised and rotated — history rewrites don't undo exposure to anyone/anything
that already fetched it.

## In this workspace specifically
- **`.mcp.json`** carries live tokens (`BITBUCKET_API_TOKEN`, `FIGMA_ACCESS_TOKEN`,
  `JIRA_API_TOKEN`). **Always gitignored.** It was copied verbatim from the your organization Android project.
- Also ignore: `.claude/settings.local.json`, `.claude/scheduled_tasks.lock`,
  `.claude/inbox|outbox|worktrees/`, `.claude/memory/` (personal/runtime), `*.log`, `.DS_Store`.

## How to apply
1. Write `.gitignore` listing secret + runtime + personal files **before** the first `git add`.
2. After `git add -A`, run `git status` and eyeball that no secret/log/lock is staged.
3. If a secret was ever committed/pushed: rotate the token, don't just delete the file.
