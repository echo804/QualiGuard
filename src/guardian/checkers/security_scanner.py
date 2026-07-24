from __future__ import annotations
import re
from guardian.checkers.base import Checker
from guardian.core.models import Issue, Severity


class SecurityScanner(Checker):
    name = "security"
    PATTERNS = [
        ("SEC001", r"password\s*=", "Hardcoded password detected", Severity.ERROR),
        ("SEC002", r"api[_-]?key\s*=", "Hardcoded API key detected", Severity.ERROR),
        ("SEC003", r"secret\s*=", "Hardcoded secret detected", Severity.ERROR),
        ("SEC004", r"eval\(", "Use of eval() can lead to code injection", Severity.ERROR),
    ]

    def check(self, file_path: str) -> list[Issue]:
        issues = []
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
            for lineno, line in enumerate(lines, 1):
                stripped = line.split("#")[0]
                for rule_id, pattern, message, severity in self.PATTERNS:
                    if re.search(pattern, stripped, re.IGNORECASE):
                        issues.append(Issue(
                            rule_id=rule_id, severity=severity,
                            message=message,
                            file_path=file_path, line=lineno,
                            checker=self.name,
                        ))
        except (OSError, UnicodeDecodeError):
            pass
        return issues
