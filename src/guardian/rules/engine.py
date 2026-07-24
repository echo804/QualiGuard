from __future__ import annotations
from guardian.core.models import Issue


class RuleEngine:
    def __init__(self, rules: list[dict] | None = None):
        self.rules = rules or []

    def evaluate(self, issues: list[Issue]) -> list[Issue]:
        """Filter and annotate issues against active rules."""
        if not self.rules:
            return issues
        active_rule_ids = {r["id"] for r in self.rules if r.get("enabled", True)}
        return [i for i in issues if i.rule_id in active_rule_ids]
