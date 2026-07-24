from __future__ import annotations
from guardian.reporters.base import Reporter
from guardian.core.models import ScanResult, Severity


class MarkdownReporter(Reporter):
    def generate(self, result: ScanResult, output_path: str | None = None) -> str:
        lines = []
        lines.append("# QualiGuard Scan Report\n")
        lines.append(f"- **Target:** {result.target}")
        lines.append(f"- **Files scanned:** {result.scanned_files}/{result.total_files}")
        lines.append(f"- **Total issues:** {len(result.issues)}")
        lines.append(f"  - Errors: {result.error_count}")
        lines.append(f"  - Warnings: {result.warning_count}")
        lines.append(f"  - Info: {result.info_count}")
        lines.append("")

        emoji = {"error": "🔴", "warning": "🟡", "info": "🔵"}
        for i, issue in enumerate(result.issues, 1):
            label = issue.severity.value.upper()
            em = emoji.get(issue.severity.value, "")
            lines.append(f"### {em} [{label}] {issue.rule_id}")
            lines.append(f"- **Message:** {issue.message}")
            lines.append(f"- **File:** {issue.file_path}")
            lines.append(f"- **Line:** {issue.line}")
            if issue.suggestion:
                lines.append(f"- **Suggestion:** {issue.suggestion}")
            lines.append("")

        output = "\n".join(lines)
        if output_path:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(output)
        return output
