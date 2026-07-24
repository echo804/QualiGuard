from __future__ import annotations
from abc import ABC, abstractmethod
from guardian.core.models import Issue
from guardian.rules.engine import RuleEngine


class Checker(ABC):
    def __init__(self, rule_engine: RuleEngine | None = None):
        self.rule_engine = rule_engine

    @abstractmethod
    def check(self, file_path: str) -> list[Issue]:
        ...
