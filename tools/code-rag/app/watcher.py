import asyncio
from pathlib import Path

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from .config import cfg
from .indexer import index_paths


class Handler(FileSystemEventHandler):
    def __init__(self):
        self.pending: set[str] = set()

    def on_any_event(self, event):
        if event.is_directory:
            return
        p = Path(event.src_path)
        if p.suffix in cfg.include_ext and not any(d in p.parts for d in cfg.exclude_dirs):
            self.pending.add(str(p.relative_to(cfg.repo_root)))


async def run():
    await index_paths()
    handler = Handler()
    observer = Observer()
    observer.schedule(handler, cfg.repo_root, recursive=True)
    observer.start()
    print("[watch] watching for changes", flush=True)
    try:
        while True:
            await asyncio.sleep(3)
            if handler.pending:
                batch = list(handler.pending)
                handler.pending = set()
                await index_paths(batch)
    finally:
        observer.stop()
        observer.join()


if __name__ == "__main__":
    asyncio.run(run())
