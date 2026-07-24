from __future__ import annotations
import subprocess
from guardian.fixers.base import Fixer
from guardian.core.models import Issue


class PythonFixer(Fixer):
    def can_fix(self, issue: Issue) -> bool:
        return issue.checker == "style" and issue.file_path.endswith(".py")

    def fix(self, file_path: str, issue: Issue) -> str | None:
        try:
            subprocess.run(
                ["ruff", "check", "--fix", "--unsafe-fixes", file_path],
                capture_output=True, text=True, timeout=30,
            )
            return f"Fixed {issue.rule_id} in {file_path}:{issue.line}"
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return None
