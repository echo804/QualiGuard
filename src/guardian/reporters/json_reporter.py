from __future__ import annotations
import json
from guardian.reporters.base import Reporter
from guardian.core.models import ScanResult, Severity


class JsonReporter(Reporter):
    def generate(self, result: ScanResult, output_path: str | None = None) -> str:
        data = {
            "tool": {"name": "QualiGuard", "version": "0.1.0"},
            "target": result.target,
            "summary": {
                "total_files": result.total_files,
                "scanned_files": result.scanned_files,
                "total_issues": len(result.issues),
                "errors": result.error_count,
                "warnings": result.warning_count,
                "info": result.info_count,
            },
            "issues": [
                {
                    "rule_id": i.rule_id,
                    "severity": i.severity.value,
                    "message": i.message,
                    "file_path": i.file_path,
                    "line": i.line,
                    "column": i.column,
                    "end_line": i.end_line,
                    "suggestion": i.suggestion,
                    "checker": i.checker,
                }
                for i in result.issues
            ],
        }
        output = json.dumps(data, ensure_ascii=False, indent=2)
        if output_path:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(output)
        return output
