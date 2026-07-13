import subprocess

from app import gitignore
from app.gitignore import _ignored_set, is_ignored


def _git(repo, *args):
    subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True)


def _init_repo(repo):
    repo.mkdir(exist_ok=True)
    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "test@example.com")
    _git(repo, "config", "user.name", "test")


def test_ignored_file_detected(tmp_path):
    _init_repo(tmp_path)
    (tmp_path / ".gitignore").write_text("secret.json\n.env\n", encoding="utf-8")
    (tmp_path / "secret.json").write_text("{}", encoding="utf-8")
    (tmp_path / "main.py").write_text("x = 1\n", encoding="utf-8")

    _ignored_set.cache_clear()
    assert is_ignored(str(tmp_path), "secret.json")
    assert not is_ignored(str(tmp_path), "main.py")


def test_nested_gitignore_honored(tmp_path):
    _init_repo(tmp_path)
    sub = tmp_path / "service"
    sub.mkdir()
    (sub / ".gitignore").write_text("service-account.json\n", encoding="utf-8")
    (sub / "service-account.json").write_text("{}", encoding="utf-8")
    (sub / "main.py").write_text("x = 1\n", encoding="utf-8")

    _ignored_set.cache_clear()
    assert is_ignored(str(tmp_path), "service/service-account.json")
    assert not is_ignored(str(tmp_path), "service/main.py")


def test_tracked_file_matching_later_gitignore_rule_stays_visible(tmp_path):
    _init_repo(tmp_path)
    (tmp_path / "config.json").write_text("{}", encoding="utf-8")
    _git(tmp_path, "add", "config.json")
    _git(tmp_path, "commit", "-q", "-m", "init")
    (tmp_path / ".gitignore").write_text("config.json\n", encoding="utf-8")

    _ignored_set.cache_clear()
    # git doesn't retroactively hide already-tracked files just because .gitignore
    # was added later — matches git's own semantics, not a bug in our wrapper.
    assert not is_ignored(str(tmp_path), "config.json")


def test_non_git_directory_fails_open(tmp_path):
    (tmp_path / "whatever.json").write_text("{}", encoding="utf-8")
    _ignored_set.cache_clear()
    assert not is_ignored(str(tmp_path), "whatever.json")


def test_ls_files_timeout_retries_then_warns_loudly(tmp_path, monkeypatch, capsys):
    _init_repo(tmp_path)
    monkeypatch.setattr(gitignore, "_is_git_repo", lambda root: True)

    calls = {"n": 0}

    def fake_run(cmd, **kwargs):
        calls["n"] += 1
        raise subprocess.TimeoutExpired(cmd=cmd, timeout=180)

    monkeypatch.setattr(subprocess, "run", fake_run)
    _ignored_set.cache_clear()

    assert not is_ignored(str(tmp_path), "secret.json")
    assert calls["n"] == 2  # one retry, not silently swallowed on the first failure
    out = capsys.readouterr().out
    assert "WARNING" in out and "RESPECT_GITIGNORE is NOT active" in out
