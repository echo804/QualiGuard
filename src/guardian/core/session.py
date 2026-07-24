from __future__ import annotations
from pathlib import Path
from guardian.config.loader import load_config
from guardian.core.models import ScanResult


class Session:
    def __init__(self, target: str, config_path: str | None = None):
        self.target = target
        self.config = load_config(config_path)

    def create_result(self) -> ScanResult:
        return ScanResult(target=self.target)
