from __future__ import annotations
from guardian.reporters.base import Reporter
from guardian.core.models import ScanResult, Severity
from guardian.knowledge import RULE_ADVICE

# ANSI color codes for terminal output
_GREEN = chr(27) + "[32m"
_YELLOW = chr(27) + "[33m"
_RESET = chr(27) + "[0m"
_BOLD = chr(27) + "[1m"


class TerminalReporter(Reporter):
    def generate(self, result: ScanResult, output_path: str | None = None) -> str:
        sep = "-" * 50
        lines = [sep]
        lines.append("  QualiGuard Scan Report")
        lines.append(sep)
        lines.append("  Target: " + self._safe(result.target))
        lines.append("  Files scanned: " + str(result.scanned_files) + "/" + str(result.total_files))
        lines.append("  Issues found: " + str(len(result.issues)))
        lines.append("    Errors:   " + str(result.error_count))
        lines.append("    Warnings: " + str(result.warning_count))
        lines.append("    Info:     " + str(result.info_count))
        lines.append(sep)

        if not result.issues:
            lines.append("  No issues found. Code looks clean!")
            lines.append(sep)
            return chr(10).join(lines)

        # Detailed issue list with grouping
        # Group repeated INFO issues by (rule_id, file_path) to reduce noise
        from collections import Counter
        group_key = lambda iss: (iss.rule_id, iss.severity.value, iss.file_path, iss.message.split("`")[0])
        info_counter: Counter = Counter()
        info_samples = {}
        single_issues = []
        for issue in result.issues:
            if issue.severity.value == "info":
                key = group_key(issue)
                info_counter[key] += 1
                if key not in info_samples:
                    info_samples[key] = issue
            else:
                single_issues.append(issue)

        idx = 0
        # Show ERROR and WARNING individually
        for issue in single_issues:
            idx += 1
            label = {"error": "ERROR", "warning": "WARN"}[issue.severity.value]
            lines.append("")
            tag = ""
            if self._is_fixable(issue):
                tag = _GREEN + " [AUTO-FIX]" + _RESET
            lines.append("  #" + str(idx) + " [" + label + "] " + issue.rule_id + tag)
            lines.append("  Message: " + self._safe(issue.message))
            lines.append("  File: " + self._safe(issue.file_path) + ":" + str(issue.line))
            sug = issue.suggestion
            if sug and sug.strip() and sug.strip() not in ("Fix:", "Fix: "):
                lines.append("  Suggestion: " + self._safe(sug))
            advice_text = self._format_advice(issue.rule_id, issue.severity.value)
            if advice_text:
                lines.append(advice_text)

        # Show grouped INFO issues
        for key, count in sorted(info_counter.items(), key=lambda x: x[0][0]):
            rule_id, sev, fpath, msg_prefix = key
            sample = info_samples[key]
            idx += 1
            label_str = "INFO"
            count_str = " x" + str(count) if count > 1 else ""
            lines.append("")
            grp_tag = ""
            if self._is_fixable(sample):
                grp_tag = _GREEN + " [AUTO-FIX]" + _RESET
            lines.append("  #" + str(idx) + " [" + label_str + "] " + rule_id + count_str + grp_tag)
            lines.append("  Message: " + self._safe(sample.message))
            lines.append("  File: " + self._safe(fpath) + ":" + str(sample.line))
            sug = sample.suggestion
            if sug and sug.strip() and sug.strip() not in ("Fix:", "Fix: "):
                lines.append("  Suggestion: " + self._safe(sug))
            advice_text = self._format_advice(rule_id, sev)
            if advice_text:
                lines.append(advice_text)

        lines.append("")
        lines.append(sep)
        lines.append("  Summary")
        lines.append(sep)

        # Summary counts
        total = len(result.issues)
        e = result.error_count
        w = result.warning_count
        i = result.info_count
        summary_parts = []
        if e:
            summary_parts.append(str(e) + " error" + ("s" if e > 1 else ""))
        if w:
            summary_parts.append(str(w) + " warning" + ("s" if w > 1 else ""))
        if i:
            summary_parts.append(str(i) + " info")
        summary_line = ", ".join(summary_parts) if summary_parts else "0 issues"
        lines.append("  Total: " + str(total) + " issue" + ("s" if total != 1 else "") + " (" + summary_line + ")")
        lines.append("")

        # Error locations (for easy navigation)
        error_issues = [iss for iss in result.issues if iss.severity.value == "error"]
        warning_issues = [iss for iss in result.issues if iss.severity.value == "warning"]

        if error_issues:
            lines.append("  Error locations (fix these first):")
            for issue in error_issues:
                loc = self._safe(issue.file_path) + ":" + str(issue.line)
                msg = self._safe(issue.message[:60])
                lines.append("    " + loc + "  -  " + msg)
            lines.append("")

        if warning_issues:
            lines.append("  Warning locations:")
            for issue in warning_issues:
                loc = self._safe(issue.file_path) + ":" + str(issue.line)
                msg = self._safe(issue.message[:60])
                lines.append("    " + loc + "  -  " + msg)
            lines.append("")

        # All files with issues
        files_with_issues = {}
        for issue in result.issues:
            fp = self._safe(issue.file_path)
            if fp not in files_with_issues:
                files_with_issues[fp] = 0
            files_with_issues[fp] += 1

        if len(files_with_issues) > 0:
            lines.append("  Files with issues:")
            for fp, count in sorted(files_with_issues.items()):
                lines.append("    " + fp + "  (" + str(count) + " issue" + ("s" if count > 1 else "") + ")")
            lines.append("")

        # Action tips
        lines.append("  Tips:")
        lines.append("    " + _GREEN + "[AUTO-FIX]" + _RESET + " = can be auto-fixed with /fix")
        if result.error_count > 0:
            lines.append("    - Fix errors first, then re-scan")
        if any(issue.severity.value == "warning" for issue in result.issues):
            lines.append("    - Address warnings to improve code quality")
        lines.append("    - Use /fix to auto-fix fixable issues")
        lines.append("    - Use /read <file> to examine a file in detail")
        lines.append("    - Use /report <path> to generate an HTML report")

        lines.append("")
        lines.append(sep)
        return chr(10).join(lines)

    @staticmethod
    def _is_fixable(issue) -> bool:
        """Check if an issue can be auto-fixed by /fix."""
        return issue.checker == "style" and hasattr(issue, "file_path") and issue.file_path.endswith(".py")

    @staticmethod
    def _format_advice(rule_id: str, severity: str = "info") -> str:
        """Append Chinese explanation and fix suggestion for a rule.
        Only shown for ERROR and WARNING (INFO is too noisy)."""
        if severity == "info":
            return ""
        advice = RULE_ADVICE.get(rule_id)
        if not advice:
            for key, val in RULE_ADVICE.items():
                rule_stripped = rule_id.rstrip("x").rstrip("*")
                key_stripped = key.rstrip("*")
                if rule_stripped.startswith(key_stripped[:4]) and len(rule_stripped) >= len(key_stripped[:4]):
                    advice = val
                    break
            if not advice:
                return ""
        title = advice.get("title", "")
        why = advice.get("why", "")
        fix = advice.get("fix", "")
        lines = []
        lines.append("  |")
        lines.append("  +-- " + title)
        if why:
            lines.append("  |   " + why)
        if fix:
            lines.append("  |")
            lines.append("  +>> " + fix)
        lines.append("  |")
        return chr(10).join(lines)

    @staticmethod
    def _safe(text: str) -> str:
        return text
