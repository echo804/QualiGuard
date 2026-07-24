"""Test TerminalReporter output format."""
from guardian.reporters.terminal import TerminalReporter
from guardian.core.models import ScanResult, Issue, Severity


def _make_issue(rule_id, severity, message="test msg", file_path="/test.py",
                line=1, checker="test", suggestion=""):
    sev = Severity.ERROR if severity == "error" else Severity.WARNING if severity == "warning" else Severity.INFO
    return Issue(rule_id=rule_id, severity=sev, message=message,
                 file_path=file_path, line=line, checker=checker, suggestion=suggestion)


def test_report_header():
    result = ScanResult(target="/test.py")
    result.scanned_files = result.total_files = 1
    report = TerminalReporter().generate(result)
    assert "QualiGuard Scan Report" in report
    assert "No issues found" in report


def test_report_counts():
    result = ScanResult(target="/test.py")
    result.scanned_files = result.total_files = 1
    result.issues = [
        _make_issue("SEC001", "error"), _make_issue("STA001", "warning"), _make_issue("STYF841", "info"),
    ]
    report = TerminalReporter().generate(result)
    assert "Issues found: 3" in report
    assert "Errors:   1" in report


def test_summary_section():
    result = ScanResult(target="/test.py")
    result.scanned_files = result.total_files = 1
    result.issues = [_make_issue("SEC001", "error", line=5)]
    report = TerminalReporter().generate(result)
    assert "Summary" in report
    assert "Error locations" in report


def test_fixable_marker():
    result = ScanResult(target="/test.py")
    result.scanned_files = result.total_files = 1
    result.issues = [_make_issue("STYF841", "info", checker="style", file_path="/test.py")]
    report = TerminalReporter().generate(result)
    assert "AUTO-FIX" in report


def test_non_fixable_no_marker():
    result = ScanResult(target="/test.py")
    result.scanned_files = result.total_files = 1
    result.issues = [_make_issue("SEC001", "error", checker="security")]
    report = TerminalReporter().generate(result)
    for line in report.split("\n"):
        if "SEC001" in line or "ERROR" in line:
            assert "AUTO-FIX" not in line, f"Non-fixable issue should not show AUTO-FIX marker: {line}"
