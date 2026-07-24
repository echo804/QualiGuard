from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path


class Severity(Enum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


@dataclass
class Issue:
    rule_id: str
    severity: Severity
    message: str
    file_path: str
    line: int
    column: int = 0
    end_line: int | None = None
    suggestion: str | None = None
    checker: str | None = None


@dataclass
class ScanResult:
    target: str
    issues: list[Issue] = field(default_factory=list)
    total_files: int = 0
    scanned_files: int = 0
    duration_ms: int = 0

    @property
    def error_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == Severity.ERROR)

    @property
    def warning_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == Severity.WARNING)

    @property
    def info_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == Severity.INFO)
