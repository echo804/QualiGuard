from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class Settings:
    checkers: list[str] = field(default_factory=lambda: ["static", "style", "security", "complexity", "dependency"])
    rules: list[str] = field(default_factory=list)
    ignore_patterns: list[str] = field(default_factory=list)
    max_line_length: int = 88
    output_format: str = "terminal"
    output_path: str | None = None
    verbose: bool = False
    threads: int = 4
