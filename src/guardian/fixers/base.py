from __future__ import annotations
from abc import ABC, abstractmethod
from guardian.core.models import Issue


class Fixer(ABC):
    @abstractmethod
    def can_fix(self, issue: Issue) -> bool:
        ...

    @abstractmethod
    def fix(self, file_path: str, issue: Issue) -> str | None:
        ...
