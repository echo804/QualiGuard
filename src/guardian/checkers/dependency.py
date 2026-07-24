from __future__ import annotations
import re
from guardian.checkers.base import Checker
from guardian.core.models import Issue, Severity


class DependencyChecker(Checker):
    name = "dependency"
    KNOWN_VULNERABLE = {
        "requests": ("<2.32.0", "CVE-2024-XXXX"),
        "urllib3": ("<2.2.2", "CVE-2024-XXXX"),
        "flask": ("<3.0.0", "CVE-2024-XXXX"),
        "django": ("<5.0.0", "CVE-2024-XXXX"),
    }

    def check(self, file_path: str) -> list[Issue]:
        basename = file_path.replace("\\", "/").rsplit("/", 1)[-1]
        if basename not in ("requirements.txt", "Pipfile", "pyproject.toml"):
            return []
        issues = []
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            for pkg, (version, cve) in self.KNOWN_VULNERABLE.items():
                escaped_version = version.replace('.', '\\.')
                pattern = rf"^{pkg}[=<>]{{1,2}}{escaped_version}"
                if re.search(pattern, content, re.MULTILINE):
                    issues.append(Issue(
                        rule_id="DEP001", severity=Severity.WARNING,
                        message=f"Vulnerable dependency {pkg}{version} ({cve})",
                        file_path=file_path, line=0,
                        checker=self.name,
                        suggestion=f"Upgrade {pkg} to a newer version",
                    ))
        except OSError:
            pass
        return issues
