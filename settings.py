# codex-task: Create a Settings class using Pydantic.
# It should hold: source folder, rules list, monitor_enabled, start_on_boot.
# Provide load() and save() methods to read/write ~/.file_sorter/settings.json

from pydantic import BaseModel
from typing import List, Dict
import json
import os

CONFIG_PATH = os.path.expanduser('~/.file_sorter/settings.json')


class Settings(BaseModel):
    source: str = ''
    rules: List[Dict] = []
    monitor_enabled: bool = False
    start_on_boot: bool = False

    @classmethod
    def load(cls):
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, 'r') as f:
                data = json.load(f)
            return cls(**data)
        return cls()

    def save(self):
        os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
        with open(CONFIG_PATH, 'w') as f:
            json.dump(self.dict(), f, indent=2)
