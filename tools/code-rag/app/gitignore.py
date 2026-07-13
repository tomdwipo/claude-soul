import subprocess
from functools import lru_cache


def _is_git_repo(repo_root: str) -> bool:
    try:
        result = subprocess.run(
            ["git", "-C", repo_root, "rev-parse", "--is-inside-work-tree"],
            capture_output=True,
            timeout=10,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return False
    return result.returncode == 0


@lru_cache(maxsize=8)
def _ignored_set(repo_root: str) -> frozenset:
    """Authoritative git-ignored relative paths under repo_root, via `git ls-files`.

    Delegates to git itself (not a hand-rolled .gitignore parser) so nested .gitignore
    files, global excludes, and .git/info/exclude are all honored exactly as git sees them.
    Cached for the process lifetime: a mid-run `.gitignore` edit needs a restart to pick up.

    Fails open (empty set, no warning) if `repo_root` isn't a git repo at all — that's a
    legitimate case (non-git checkout), not a failure.

    If it IS a git repo but `ls-files` itself fails or times out (e.g. a large repo's first
    scan over a slow bind mount, cold filesystem cache), this is NOT the same as "no rules
    to apply" — silently returning empty here would silently re-open exactly the secret-leak
    gap this module exists to close. So: generous timeout, one retry, and if it still fails,
    print a loud warning (visible in `docker logs`) before falling back — a failure here must
    never be invisible, unlike this codebase's usual best-effort fail-open elsewhere.
    """
    if not _is_git_repo(repo_root):
        return frozenset()

    last_err: Exception | None = None
    for attempt in range(2):
        try:
            result = subprocess.run(
                ["git", "-C", repo_root, "ls-files", "--others", "--ignored", "--exclude-standard", "-z"],
                capture_output=True,
                timeout=180,
                check=False,
            )
        except (OSError, subprocess.SubprocessError) as e:
            last_err = e
            continue
        if result.returncode != 0:
            last_err = RuntimeError(result.stderr.decode("utf-8", errors="replace").strip())
            continue
        raw = result.stdout.decode("utf-8", errors="replace")
        return frozenset(p for p in raw.split("\0") if p)

    print(
        f"[gitignore] WARNING: `git ls-files --ignored` failed after retry ({last_err!r}) — "
        "RESPECT_GITIGNORE is NOT active this run, gitignored secrets could get indexed. "
        "Check `git -C <repo_root> ls-files --others --ignored --exclude-standard` manually.",
        flush=True,
    )
    return frozenset()


def is_ignored(repo_root: str, rel_path: str) -> bool:
    return rel_path in _ignored_set(repo_root)
