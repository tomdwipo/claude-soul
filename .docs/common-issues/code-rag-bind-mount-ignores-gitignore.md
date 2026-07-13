# A repo bind-mount reads the filesystem, not git — respect `.gitignore` explicitly, don't assume it

**Subject:** docker / security · **Settled by:** a live incident — the very first index run.

## Rule
A dev tool that reads a repo via a `docker volume`/bind mount sees the **filesystem**, not git.
`.gitignore` only protects `git add`/`commit`/`push` — it does nothing on its own against any local
process (indexer, linter, backup script, …) that walks the working tree directly. If that tool's
output can leave the machine, get stored unencrypted, or be queried by something else (a vector DB,
a build artifact, a log), a gitignored secret is exposed exactly as if it were tracked.

## What happened in `tools/code-rag`
First index on a real multi-project workspace embedded `.mcp.json` (live API tokens) and a
`service-account.json` (a GCP private key) into the local Qdrant collection, in plaintext — both
files were correctly `.gitignore`d, but the watcher/`mcp-server` mount the repo `:ro` and match
purely on `INCLUDE_EXT`/`EXCLUDE_DIRS`/`EXCLUDE_FILES` (`app/indexer.py`, `app/watcher.py`), none of
which consulted git at all.

## Fix
Added `RESPECT_GITIGNORE` (default `true`, `app/config.py` + `app/gitignore.py`): both the watcher
and the full-index pass now ask `git ls-files --others --ignored --exclude-standard` (delegated to
git itself, not a hand-rolled `.gitignore` parser — nested `.gitignore`, global excludes, and
`.git/info/exclude` all honored for free) and skip anything git would ignore. Fails open (indexes
normally) if the mounted path isn't a git repo, so it never silently blocks a non-git checkout.
`EXCLUDE_FILES` stays as a second, independent layer (its default now also lists `.mcp.json` — this
tool's own config file, so a fresh install is safe even with git-ignore checking off).

## How to apply elsewhere
Before wiring ANY tool that walks a working tree by filesystem path (indexers, semantic search,
backup/sync scripts, log shippers) rather than through git — ask: does this tool's output leave the
sandbox, land in a database, or get served to another process/agent? If yes, don't rely on
`.gitignore` implicitly; either make the tool git-ignore-aware (as done here) or explicitly enumerate
what to exclude — and verify empirically (watch the first run's logs / list what actually got
ingested) rather than assuming a `.gitignore` "already handles it."
