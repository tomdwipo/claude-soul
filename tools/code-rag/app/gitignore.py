import subprocess
from functools import lru_cache


@lru_cache(maxsize=8)
def _ignored_set(repo_root: str) -> frozenset:
    """Authoritative git-ignored relative paths under repo_root, via `git ls-files`.

    Delegates to git itself (not a hand-rolled .gitignore parser) so nested .gitignore
    files, global excludes, and .git/info/exclude are all honored exactly as git sees them.
    Fails open (empty set) if repo_root isn't a git repo or `git` isn't available — the
    existing INCLUDE_EXT/EXCLUDE_DIRS/EXCLUDE_FILES filters still apply regardless.
    Cached for the process lifetime: a mid-run `.gitignore` edit needs a restart to pick up.
    """
    try:
        result = subprocess.run(
            ["git", "-C", repo_root, "ls-files", "--others", "--ignored", "--exclude-standard", "-z"],
            capture_output=True,
            timeout=30,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return frozenset()
    if result.returncode != 0:
        return frozenset()
    raw = result.stdout.decode("utf-8", errors="replace")
    return frozenset(p for p in raw.split("\0") if p)


def is_ignored(repo_root: str, rel_path: str) -> bool:
    return rel_path in _ignored_set(repo_root)
