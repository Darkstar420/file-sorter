# codex-task: Create a system tray icon using pystray.
# Menu: Toggle Monitor (on/off), Run Now, Open GUI, Quit
# Icon should update based on monitor state (green/red)

import threading
from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw

from mover import move_files
from monitor import start_monitor
from settings import Settings


class Tray:
    def __init__(self, settings: Settings, open_gui_callback=None):
        self.settings = settings
        self.open_gui_callback = open_gui_callback
        self.observer = None
        self.icon = Icon("FileSorter")
        self.icon.menu = Menu(
            MenuItem("Toggle Monitor", self.toggle_monitor),
            MenuItem("Run Now", self.run_now),
            MenuItem("Open GUI", self.open_gui),
            MenuItem("Quit", self.quit)
        )
        self.update_icon()

    def _create_image(self, color: str):
        image = Image.new('RGB', (16, 16), color)
        d = ImageDraw.Draw(image)
        d.rectangle([0, 0, 15, 15], fill=color)
        return image

    def update_icon(self):
        color = 'green' if self.observer else 'red'
        self.icon.icon = self._create_image(color)

    def toggle_monitor(self, icon, item):
        if self.observer:
            self.observer.stop()
            self.observer.join()
            self.observer = None
        else:
            self.observer = start_monitor(self.settings.source, self.settings.rules)
        self.update_icon()

    def run_now(self, icon, item):
        move_files(self.settings.source, self.settings.rules)

    def open_gui(self, icon, item):
        if self.open_gui_callback:
            threading.Thread(target=self.open_gui_callback).start()

    def quit(self, icon, item):
        if self.observer:
            self.observer.stop()
            self.observer.join()
        self.icon.stop()

    def run(self):
        self.icon.run_detached()
