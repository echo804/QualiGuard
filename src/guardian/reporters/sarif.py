from __future__ import annotations
import json
from guardian.reporters.base import Reporter
from guardian.core.models import ScanResult, Severity


class SarifReporter(Reporter):
    LEVEL_MAP = {
        Severity.ERROR: "error",
        Severity.WARNING: "warning",
        Severity.INFO: "note",
    }

    def generate(self, result: ScanResult, output_path: str | None = None) -> str:
        rules = {}
        results = []
        for issue in result.issues:
            rule_id = issue.rule_id
            if rule_id not in rules:
                rules[rule_id] = {
                    "id": rule_id,
                    "shortDescription": {"text": issue.message},
                    "properties": {"severity": issue.severity.value},
                }

            results.append({
                "ruleId": rule_id,
                "level": self.LEVEL_MAP.get(issue.severity, "note"),
                "message": {"text": issue.message},
                "locations": [
                    {
                        "physicalLocation": {
                            "artifactLocation": {"uri": issue.file_path},
                            "region": {
                                "startLine": issue.line,
                                "startColumn": issue.column or 1,
                            },
                        }
                    }
                ],
                "properties": {
                    "checker": issue.checker,
                    "suggestion": issue.suggestion,
                },
            })

        sarif = {
            "": "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/master/Schemata/sarif-schema-2.1.0.json",
            "version": "2.1.0",
            "runs": [
                {
                    "tool": {
                        "driver": {
                            "name": "QualiGuard",
                            "version": "0.1.0",
                            "rules": list(rules.values()),
                        }
                    },
                    "results": results,
                }
            ],
        }

        output = json.dumps(sarif, ensure_ascii=False, indent=2)
        if output_path:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(output)
        return output
