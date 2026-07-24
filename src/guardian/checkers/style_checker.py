from __future__ import annotations
import subprocess
import json
from guardian.checkers.base import Checker
from guardian.core.models import Issue, Severity


class StyleChecker(Checker):
    name = "style"

    def check(self, file_path: str) -> list[Issue]:
        if not file_path.endswith(".py"):
            return []
        try:
            result = subprocess.run(
                ["ruff", "check", "--output-format", "json", file_path],
                capture_output=True, text=True, timeout=30,
            )
            if not result.stdout.strip():
                return []
            data = json.loads(result.stdout)
            issues = []
            for item in data:
                code = item.get("code", "000")
                level = item.get("level", "")
                issues.append(Issue(
                    rule_id=f"STY{code}",
                    severity=Severity.WARNING if level == "error" else Severity.INFO,
                    message=item.get("message", ""),
                    file_path=item.get("filename", file_path),
                    line=item.get("line", 0),
                    column=item.get("column", 0),
                    checker=self.name,
                    suggestion=f"Fix: {(item.get('fix') or {}).get('message', '')}",
                ))
            return issues
        except (FileNotFoundError, subprocess.TimeoutExpired, json.JSONDecodeError):
            return []
