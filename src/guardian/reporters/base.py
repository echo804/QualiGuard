from __future__ import annotations
from abc import ABC, abstractmethod
from guardian.core.models import ScanResult


class Reporter(ABC):
    @abstractmethod
    def generate(self, result: ScanResult, output_path: str | None = None) -> str:
        """Generate report and return as string."""
        ...
