# codex-task: Use watchdog to monitor a folder. On new file creation,
# call move_files(source_path, rules). De-bounce noisy temp files (like .crdownload).

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
from typing import List

from mover import move_files


def _is_temporary(name: str) -> bool:
    return name.endswith('.crdownload') or name.endswith('.tmp') or name.startswith('~')


class _NewFileHandler(FileSystemEventHandler):
    def __init__(self, source: str, rules: List[dict]):
        super().__init__()
        self.source = source
        self.rules = rules

    def on_created(self, event):
        if event.is_directory:
            return
        if _is_temporary(os.path.basename(event.src_path)):
            return
        move_files(self.source, self.rules)


def start_monitor(source_path: str, rules: list):
    observer = Observer()
    handler = _NewFileHandler(source_path, rules)
    observer.schedule(handler, source_path, recursive=False)
    observer.start()
    return observer
