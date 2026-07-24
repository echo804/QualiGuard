from __future__ import annotations
import ast
from guardian.checkers.base import Checker
from guardian.core.models import Issue, Severity


class ComplexityAnalyzer(Checker):
    name = "complexity"
    THRESHOLD = 10

    def check(self, file_path: str) -> list[Issue]:
        if not file_path.endswith(".py"):
            return []
        issues = []
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                tree = ast.parse(f.read(), filename=file_path)
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    score = self._cyclomatic_complexity(node)
                    if score > self.THRESHOLD:
                        issues.append(Issue(
                            rule_id="CPX001", severity=Severity.WARNING,
                            message=f"Cyclomatic complexity of '{node.name}' is {score} (threshold: {self.THRESHOLD})",
                            file_path=file_path, line=node.lineno,
                            checker=self.name,
                        ))
        except (SyntaxError, OSError):
            pass
        return issues

    def _cyclomatic_complexity(self, node: ast.AST) -> int:
        score = 1
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.AsyncFor,
                                  ast.ExceptHandler, ast.With, ast.AsyncWith,
                                  ast.Assert)):
                score += 1
            elif isinstance(child, ast.BoolOp):
                score += len(child.values) - 1
            elif isinstance(child, (ast.Match,)):
                score += 1
        return score
