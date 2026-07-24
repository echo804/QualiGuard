from __future__ import annotations
from pathlib import Path
from guardian.checkers.base import Checker
from guardian.core.models import ScanResult, Issue


class Scheduler:
    def __init__(self, checkers: list[Checker]):
        self.checkers = checkers

    def run(self, target: str, result: ScanResult) -> None:
        files = self._collect_files(target)
        result.total_files = len(files)
        for file in files:
            for checker in self.checkers:
                issues = checker.check(str(file))
                result.issues.extend(issues)
            result.scanned_files += 1

    def _collect_files(self, target: str) -> list[Path]:
        path = Path(target)
        if path.is_file():
            return [path]
        extensions = (".py", ".js", ".ts", ".jsx", ".tsx")
        return [f for f in path.rglob("*") if f.suffix in extensions and not f.name.startswith(".")]
