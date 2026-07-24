from __future__ import annotations
from guardian.checkers.base import Checker
from guardian.core.models import Issue, Severity


class StaticAnalyzer(Checker):
    name = "static"

    def check(self, file_path: str) -> list[Issue]:
        if not file_path.endswith(".py"):
            return []
        import ast
        issues = []
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                tree = ast.parse(f.read(), filename=file_path)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and len(node.body) > 50:
                    issues.append(Issue(
                        rule_id="STA001", severity=Severity.WARNING,
                        message=f"Function '{node.name}' has {len(node.body)} statements, consider refactoring",
                        file_path=file_path, line=node.lineno,
                        checker=self.name,
                    ))
        except SyntaxError as e:
            issues.append(Issue(
                rule_id="STA000", severity=Severity.ERROR,
                message=f"Syntax error: {e}",
                file_path=file_path, line=e.lineno or 0,
                checker=self.name,
            ))
        return issues
