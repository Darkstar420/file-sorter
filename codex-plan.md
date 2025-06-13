# Codex Build Plan – File Sorter & Monitor Utility

## Purpose
Desktop utility that tidies a chosen folder (e.g. user's Desktop) by moving files into destination roots, with YYYY/MM/DD sub-folders. Includes a monitor mode with a system-tray on/off switch.

## Key Features
1. **Sleek GUI (Qt/PySide6)**
   - “Source Folder” picker
   - Table of “Rules” → each rule = file-pattern (extension wildcards) + Destination Root
   - Buttons: Add Rule, Remove Rule, Save Config, Run Once, Enable Monitor
   - Dark & Light theme auto-detect
   - Drag-and-drop files previews

2. **Rule Engine (`mover.py`)**
   - For every file in source, match first rule pattern.
   - Build path: `<dest_root>/<YYYY>/<MonthName>/<DD>/`  
     e.g. `D:\Docs\2025/March/13/report.pdf`
   - Create directories if missing.
   - If duplicate name exists, append `_(n)`.

3. **Monitor Mode (`monitor.py`)**
   - Uses watchdog Observer to watch source folder for `on_created`.
   - Debounce bursts (e.g. browser download “.crdownload”).
   - Fires `move_file()`.

4. **System Tray (`tray.py`)**
   - Icon shows green (active) / red (paused).
   - Menu: Toggle Monitor, Run Cleanup Now, Open GUI, Quit.
   - Launches on OS login if user checks “Start at boot”.

5. **Settings (`settings.py`)**
   - Pydantic model with:
     ```json
     {
       "source": "C:/Users/<name>/Desktop",
       "rules": [
         {"pattern": "*.pdf",  "dest": "D:/Docs"},
         {"pattern": "*.png;*.jpg", "dest": "D:/Pics"}
       ],
       "monitor_enabled": false,
       "start_on_boot": false
     }
     ```
   - Persisted to `~/.file_sorter/settings.json`.

6. **Cross-Platform Packaging**
   - `pyinstaller --onefile --windowed sorter/gui.py`
   - Provide build scripts for Win x64, macOS (universal), Linux AppImage.

## Non-Goals
- No cloud sync.
- No file *copying*—always move. (Future option.)
- No DB; settings only.

## Acceptance Tests
- Given a temp folder with mixed files, “Run Once” sorts correctly, dupes handled.
- Monitor moves a new `.pdf` within 1 s.
- Toggling tray icon pauses observer.

## Stretch Goals (later)
- Regex or MIME-type rules.
- Progress bar + undo last batch.
- CLI mode (`file-sorter --once --src ...`).

