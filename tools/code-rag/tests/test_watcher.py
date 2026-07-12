import types

from app import watcher
from app.watcher import Handler


def _event(path: str, is_dir: bool = False):
    return types.SimpleNamespace(src_path=path, is_directory=is_dir)


def test_included_file_lands_in_pending(monkeypatch, tmp_path):
    monkeypatch.setattr(watcher.cfg, "repo_root", str(tmp_path))
    h = Handler()
    h.on_any_event(_event(str(tmp_path / "feature" / "Foo.kt")))
    assert "feature/Foo.kt" in h.pending


def test_excluded_dir_is_ignored(monkeypatch, tmp_path):
    monkeypatch.setattr(watcher.cfg, "repo_root", str(tmp_path))
    h = Handler()
    h.on_any_event(_event(str(tmp_path / "build" / "Generated.kt")))
    h.on_any_event(_event(str(tmp_path / "logo.png")))
    h.on_any_event(_event(str(tmp_path / "dir"), is_dir=True))
    assert h.pending == set()
