from __future__ import annotations
from guardian.fixers.base import Fixer
from guardian.core.models import Issue
from guardian.fixers.python_fixer import PythonFixer


class FixScheduler:
    def __init__(self):
        self.fixers: list[Fixer] = [PythonFixer()]

    def fix_issues(self, issues: list[Issue]) -> int:
        fixed = 0
        for issue in issues:
            for fixer in self.fixers:
                if fixer.can_fix(issue):
                    result = fixer.fix(issue.file_path, issue)
                    if result:
                        fixed += 1
                    break
        return fixed
