import os
import glob
import shutil


def move_files(source, rules):
    moved = []
    for rule in rules:
        pattern = rule.get("pattern", "*")
        dest = rule.get("dest", source)
        pattern_path = os.path.join(source, pattern)
        for file_path in glob.glob(pattern_path):
            if os.path.isfile(file_path):
                os.makedirs(dest, exist_ok=True)
                dest_path = shutil.move(file_path, dest)
                moved.append(dest_path)
    return moved
