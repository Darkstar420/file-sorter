# codex-task: Implement move_files(source: str, rules: list) that:
# - Iterates through all files in the source directory
# - Matches each file against the first rule where glob matches (e.g., *.pdf)
# - Builds the destination path: dest/YYYY/MonthName/DD/
# - Moves the file, avoids overwrites (append _1, _2 if needed)
# - Logs all moves to a list and returns it

import os
import shutil
from datetime import datetime
from pathlib import Path
from fnmatch import fnmatch


def move_files(source: str, rules: list) -> list:
    """Move files from source based on glob rules."""
    moves = []
    src_path = Path(source)
    if not src_path.exists():
        return moves

    for item in src_path.iterdir():
        if not item.is_file():
            continue

        matched_rule = None
        for rule in rules:
            pattern = rule.get("pattern")
            if pattern and fnmatch(item.name, pattern):
                matched_rule = rule
                break
        if not matched_rule:
            continue

        dest_root = Path(matched_rule.get("dest", source))
        ts = datetime.fromtimestamp(item.stat().st_mtime)
        dest_dir = dest_root / str(ts.year) / ts.strftime("%B") / f"{ts.day:02d}"
        dest_dir.mkdir(parents=True, exist_ok=True)

        dest_file = dest_dir / item.name
        counter = 1
        while dest_file.exists():
            dest_file = dest_dir / f"{item.stem}_{counter}{item.suffix}"
            counter += 1

        shutil.move(str(item), str(dest_file))
        moves.append({"src": str(item), "dest": str(dest_file)})

    return moves
