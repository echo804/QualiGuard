"""Evaluation scenarios for QualiGuard Agent.

Each scenario is a dict with:
  - id:       unique identifier
  - type:     category (security/style/complexity/report/comprehensive/error_recovery)
  - severity: difficulty (easy/medium/hard)
  - title:    short description
  - prompt:   what to ask the agent
  - setup:    list of (source, dest) file copies to prepare test env
  - expect:   criteria dict for verification
  - verify:   Python expression/callable that checks success
"""

SCENARIOS: list[dict] = []

# ===========================================================================
# Category: Security (15 scenarios)
# ===========================================================================

SEC_BASE = [
    {
        "id": "sec-001",
        "type": "security",
        "severity": "easy",
        "title": "Detect hardcoded password",
        "prompt": "Scan the target directory for hardcoded passwords. Report what you find.",
        "files": [("insecure_code.py", "target/insecure_code.py")],
        "expect": {"scan_issues_gt": 0, "contains_sec001": True},
    },
    {
        "id": "sec-002",
        "type": "security",
        "severity": "easy",
        "title": "Detect hardcoded API key",
        "prompt": "Check target/insecure_code.py for any hardcoded API keys or secrets.",
        "files": [("insecure_code.py", "target/insecure_code.py")],
        "expect": {"scan_issues_gt": 0, "contains_sec002": True},
    },
    {
        "id": "sec-003",
        "type": "security",
        "severity": "easy",
        "title": "Detect dangerous eval()",
        "prompt": "Find all dangerous eval() calls in target/insecure_code.py.",
        "files": [("insecure_code.py", "target/insecure_code.py")],
        "expect": {"scan_issues_gt": 0, "contains_sec004": True},
    },
    {
        "id": "sec-004",
        "type": "security",
        "severity": "easy",
        "title": "Full security scan of single file",
        "prompt": "Run a complete security scan on target/bad_python.py.",
        "files": [("bad_python.py", "target/bad_python.py")],
        "expect": {"scan_issues_gt": 0},
    },
    {
        "id": "sec-005",
        "type": "security",
        "severity": "medium",
        "title": "Scan multi-file project for secrets",
        "prompt": "Scan the target/ directory for all security issues (SEC* rules). List every issue found.",
        "files": [
            ("insecure_code.py", "target/app/insecure_code.py"),
            ("fixture_scan_demo.py", "target/app/utils.py"),
        ],
        "expect": {"scan_issues_gt": 0, "contains_sec001": True, "contains_sec004": True},
    },
    {
        "id": "sec-006",
        "type": "security",
        "severity": "medium",
        "title": "Explain security rule",
        "prompt": "What does rule SEC001 mean? Show me the details.",
        "files": [],
        "expect": {"rule_looked_up": True},
    },
    {
        "id": "sec-007",
        "type": "security",
        "severity": "medium",
        "title": "Explain multiple security rules",
        "prompt": "Explain the differences between SEC001, SEC002, and SEC004 rules.",
        "files": [],
        "expect": {"rule_looked_up": True, "rules_count_ge": 3},
    },
    {
        "id": "sec-008",
        "type": "security",
        "severity": "hard",
        "title": "Scan and summarize security findings",
        "prompt": "Scan the target/ directory, focus only on security issues (SEC rules). Give me a short summary of what you found, organized by severity.",
        "files": [
            ("insecure_code.py", "target/insecure_code.py"),
            ("bad_python.py", "target/bad_python.py"),
        ],
        "expect": {"scan_issues_gt": 0, "summary_provided": True},
    },
    {
        "id": "sec-009",
        "type": "security",
        "severity": "hard",
        "title": "Read file then scan it",
        "prompt": "First read target/insecure_code.py, then scan it for security issues.",
        "files": [("insecure_code.py", "target/insecure_code.py")],
        "expect": {"scan_issues_gt": 0, "file_read": True},
    },
    {
        "id": "sec-010",
        "type": "security",
        "severity": "easy",
        "title": "Security scan with filter",
        "prompt": "Only scan for SEC rules in target/.",
        "files": [("fixture_scan_demo.py", "target/fixture_scan_demo.py")],
        "expect": {"scan_issues_gt": 0},
    },
    {
        "id": "sec-011",
        "type": "security",
        "severity": "medium",
        "title": "Multi-file security inspection",
        "prompt": "Scan both target/app.py and target/utils.py for security problems. Tell me which file has more issues.",
        "files": [
            ("insecure_code.py", "target/app.py"),
            ("fixture_scan_demo.py", "target/utils.py"),
        ],
        "expect": {"scan_issues_gt": 0},
    },
    {
        "id": "sec-012",
        "type": "security",
        "severity": "medium",
        "title": "Check for syntax errors",
        "prompt": "Scan target/ for Python syntax errors.",
        "files": [
            ("fixture_syntax_error.py", "target/fixture_syntax_error.py"),
        ],
        "expect": {"scan_issues_gt": 0},
    },
    {
        "id": "sec-013",
        "type": "security",
        "severity": "hard",
        "title": "Deep security audit with read",
        "prompt": "Read target/insecure_code.py, then scan it. For each SEC issue found, read the relevant lines and explain the risk.",
        "files": [("insecure_code.py", "target/insecure_code.py")],
        "expect": {"scan_issues_gt": 0, "file_read": True},
    },
    {
        "id": "sec-014",
        "type": "security",
        "severity": "easy",
        "title": "Quick security check",
        "prompt": "Do a quick scan of target/ for any security issues.",
        "files": [("insecure_code.py", "target/insecure_code.py")],
        "expect": {"scan_issues_gt": 0},
    },
    {
        "id": "sec-015",
        "type": "security",
        "severity": "medium",
        "title": "Scan with explain combo",
        "prompt": "Scan target/ for security issues, then explain what SEC004 means.",
        "files": [("insecure_code.py", "target/insecure_code.py")],
        "expect": {"scan_issues_gt": 0, "rule_looked_up": True},
    },
]

# ===========================================================================
# Category: Style (10 scenarios)
# ===========================================================================

STY_BASE = [
    {
        "id": "sty-001",
        "type": "style",
        "severity": "easy",
        "title": "Detect long lines",
        "prompt": "Check target/bad_python.py for lines that are too long.",
        "files": [("bad_python.py", "target/bad_python.py")],
        "expect": {"scan_issues_gt": 0},
    },
    {
        "id": "sty-002",
        "type": "style",
        "severity": "easy",
        "title": "Style scan demo file",
        "prompt": "Scan target/fixture_scan_demo.py for style issues.",
        "files": [("fixture_scan_demo.py", "target/fixture_scan_demo.py")],
        "expect": {"scan_issues_gt": 0},
    },
    {
        "id": "sty-003",
        "type": "style",
        "severity": "medium",
        "title": "Full style audit",
        "prompt": "Run a complete style check on target/. Report only STY* issues.",
        "files": [
            ("bad_python.py", "target/bad_python.py"),
            ("fixture_scan_demo.py", "target/demo.py"),
        ],
        "expect": {"scan_issues_gt": 0},
    },
    {
        "id": "sty-004",
        "type": "style",
        "severity": "easy",
        "title": "Explain style rules",
        "prompt": "What kind of issues do the STY* rules check for?",
        "files": [],
        "expect": {"rule_looked_up": True},
    },
    {
        "id": "sty-005",
        "type": "style",
        "severity": "medium",
        "title": "Auto-fix style issues",
        "prompt": "Fix the style issues in target/bad_python.py.",
        "files": [("bad_python.py", "target/bad_python.py")],
        "expect": {"fix_attempted": True},
    },
    {
        "id": "sty-006",
        "type": "style",
        "severity": "hard",
        "title": "Scan, read, and explain style problems",
        "prompt": "Scan target/bad_python.py for style issues, read the file, and explain why each style issue matters.",
        "files": [("bad_python.py", "target/bad_python.py")],
        "expect": {"scan_issues_gt": 0, "file_read": True},
    },
    {
        "id": "sty-007",
        "type": "style",
        "severity": "easy",
        "title": "Style-only scan",
        "prompt": "Scan just for STY rules in target/bad_python.py.",
        "files": [("bad_python.py", "target/bad_python.py")],
        "expect": {"scan_issues_gt": 0},
    },
    {
        "id": "sty-008",
        "type": "style",
        "severity": "medium",
        "title": "Multi-file style comparison",
        "prompt": "Scan target/ and compare which file has more style issues.",
        "files": [
            ("bad_python.py", "target/file1.py"),
            ("fixture_scan_demo.py", "target/file2.py"),
        ],
        "expect": {"scan_issues_gt": 0},
    },
    {
        "id": "sty-009",
        "type": "style",
        "severity": "easy",
        "title": "Check code style of a simple file",
        "prompt": "Check the code style of target/insecure_code.py.",
        "files": [("insecure_code.py", "target/insecure_code.py")],
        "expect": {"scan_issues_gt": 0},
    },
    {
        "id": "sty-010",
        "type": "style",
        "severity": "hard",
        "title": "Fix all fixable style issues and verify",
        "prompt": "Fix all auto-fixable style issues in target/bad_python.py. Then scan again to verify the fixes worked.",
        "files": [("bad_python.py", "target/bad_python.py")],
        "expect": {"fix_attempted": True, "verification_scan": True},
    },
]

# ===========================================================================
# Category: Complexity (8 scenarios)
# ===========================================================================

CPX_BASE = [
    {
        "id": "cpx-001",
        "type": "complexity",
        "severity": "easy",
        "title": "Detect high complexity",
        "prompt": "Scan target/bad_python.py for functions with high cyclomatic complexity.",
        "files": [("bad_python.py", "target/bad_python.py")],
        "expect": {"scan_issues_gt": 0},
    },
    {
        "id": "cpx-002",
        "type": "complexity",
        "severity": "easy",
        "title": "Detect long functions",
        "prompt": "Find functions that are too long in target/bad_python.py.",
        "files": [("bad_python.py", "target/bad_python.py")],
        "expect": {"scan_issues_gt": 0},
    },
    {
        "id": "cpx-003",
        "type": "complexity",
        "severity": "medium",
        "title": "Complexity audit of demo file",
        "prompt": "Check target/fixture_scan_demo.py for complexity (CPX*) and long function (STA001) issues.",
        "files": [("fixture_scan_demo.py", "target/fixture_scan_demo.py")],
        "expect": {"scan_issues_gt": 0},
    },
    {
        "id": "cpx-004",
        "type": "complexity",
        "severity": "easy",
        "title": "Explain complexity rules",
        "prompt": "Show me the details of CPX001 and STA001 rules.",
        "files": [],
        "expect": {"rule_looked_up": True, "rules_count_ge": 2},
    },
    {
        "id": "cpx-005",
        "type": "complexity",
        "severity": "medium",
        "title": "Full complexity scan",
        "prompt": "Scan target/ for all complexity-related issues.",
        "files": [
            ("bad_python.py", "target/bad_python.py"),
            ("fixture_scan_demo.py", "target/demo.py"),
        ],
        "expect": {"scan_issues_gt": 0},
    },
    {
        "id": "cpx-006",
        "type": "complexity",
        "severity": "hard",
        "title": "Analyze and explain complexity",
        "prompt": "Scan target/ for complexity issues, read the problematic function, and explain why high complexity is bad.",
        "files": [("bad_python.py", "target/bad_python.py")],
        "expect": {"scan_issues_gt": 0, "file_read": True},
    },
    {
        "id": "cpx-007",
        "type": "complexity",
        "severity": "medium",
        "title": "CPA with style comparison",
        "prompt": "Scan target/ for both complexity and style issues. Which category has more problems?",
        "files": [("bad_python.py", "target/bad_python.py"), ("fixture_scan_demo.py", "target/demo.py")],
        "expect": {"scan_issues_gt": 0},
    },
    {
        "id": "cpx-008",
        "type": "complexity",
        "severity": "hard",
        "title": "Multi-file scan with filter",
        "prompt": "Scan target/ and only show me CPX issues. Then explain what those mean.",
        "files": [("bad_python.py", "target/bad_python.py")],
        "expect": {"scan_issues_gt": 0, "rule_looked_up": True},
    },
]

# ===========================================================================
# Category: Report Generation (5 scenarios)
# ===========================================================================

RPT_BASE = [
    {
        "id": "rpt-001",
        "type": "report",
        "severity": "medium",
        "title": "Generate terminal report",
        "prompt": "Scan target/ and generate a terminal format report.",
        "files": [("bad_python.py", "target/bad_python.py")],
        "expect": {"scan_issues_gt": 0},
    },
    {
        "id": "rpt-002",
        "type": "report",
        "severity": "medium",
        "title": "Generate JSON report",
        "prompt": "Scan the project and save the results as a JSON report.",
        "files": [("insecure_code.py", "target/insecure_code.py")],
        "expect": {"report_generated": True},
    },
    {
        "id": "rpt-003",
        "type": "report",
        "severity": "hard",
        "title": "Generate HTML report",
        "prompt": "Run a full scan of target/ and generate an HTML report file. Tell me where it was saved.",
        "files": [
            ("bad_python.py", "target/bad_python.py"),
            ("insecure_code.py", "target/insecure_code.py"),
        ],
        "expect": {"report_generated": True},
    },
    {
        "id": "rpt-004",
        "type": "report",
        "severity": "medium",
        "title": "Markdown report",
        "prompt": "Scan target/ and output the results in markdown format.",
        "files": [("bad_python.py", "target/bad_python.py")],
        "expect": {"scan_issues_gt": 0},
    },
    {
        "id": "rpt-005",
        "type": "report",
        "severity": "hard",
        "title": "Generate and explain report contents",
        "prompt": "Scan target/, generate a JSON report, then read the report and summarize the findings.",
        "files": [("bad_python.py", "target/bad_python.py"), ("insecure_code.py", "target/insecure_code.py")],
        "expect": {"report_generated": True, "file_read": True},
    },
]

# ===========================================================================
# Category: Comprehensive (7 scenarios)
# ===========================================================================

CMP_BASE = [
    {
        "id": "cmp-001",
        "type": "comprehensive",
        "severity": "hard",
        "title": "Full project quality assessment",
        "prompt": "Do a complete code quality assessment of target/. Give me an organized report with issue counts by category and severity.",
        "files": [
            ("bad_python.py", "target/src/bad_python.py"),
            ("insecure_code.py", "target/src/insecure_code.py"),
            ("fixture_scan_demo.py", "target/src/demo.py"),
        ],
        "expect": {"scan_issues_gt": 0, "summary_provided": True},
    },
    {
        "id": "cmp-002",
        "type": "comprehensive",
        "severity": "hard",
        "title": "Scan then fix",
        "prompt": "Scan target/, fix all auto-fixable issues, then scan again to confirm the fixes.",
        "files": [("bad_python.py", "target/bad_python.py")],
        "expect": {"fix_attempted": True, "verification_scan": True},
    },
    {
        "id": "cmp-003",
        "type": "comprehensive",
        "severity": "hard",
        "title": "Find and explain the worst file",
        "prompt": "Scan target/, find which file has the most issues, read that file, and explain why it has problems.",
        "files": [
            ("bad_python.py", "target/file_a.py"),
            ("insecure_code.py", "target/file_b.py"),
        ],
        "expect": {"scan_issues_gt": 0, "file_read": True},
    },
    {
        "id": "cmp-004",
        "type": "comprehensive",
        "severity": "hard",
        "title": "Quality gate check",
        "prompt": "Check if target/ passes a quality gate: no ERROR-level issues allowed. Scan and tell me if it passes.",
        "files": [
            ("insecure_code.py", "target/app.py"),
        ],
        "expect": {"scan_issues_gt": 0},
    },
    {
        "id": "cmp-005",
        "type": "comprehensive",
        "severity": "hard",
        "title": "Rule explanation workshop",
        "prompt": "Scan target/, then explain each type of issue found and how to fix it.",
        "files": [("insecure_code.py", "target/insecure_code.py")],
        "expect": {"scan_issues_gt": 0, "rule_looked_up": True},
    },
    {
        "id": "cmp-006",
        "type": "comprehensive",
        "severity": "hard",
        "title": "Multi-tool workflow",
        "prompt": "Scan target/ for all issues. Read the file with the most problems. Then explain the rules involved.",
        "files": [
            ("bad_python.py", "target/bad_python.py"),
            ("fixture_scan_demo.py", "target/demo.py"),
        ],
        "expect": {"scan_issues_gt": 0, "file_read": True, "rule_looked_up": True},
    },
    {
        "id": "cmp-007",
        "type": "comprehensive",
        "severity": "hard",
        "title": "Priority-based scan",
        "prompt": "Scan target/, then focus on the most severe (ERROR) issues first. Read those files and explain the top 3 risks.",
        "files": [
            ("insecure_code.py", "target/insecure_code.py"),
            ("bad_python.py", "target/bad_python.py"),
        ],
        "expect": {"scan_issues_gt": 0, "file_read": True},
    },
]

# ===========================================================================
# Category: Error Recovery (5 scenarios)
# ===========================================================================

ERR_BASE = [
    {
        "id": "err-001",
        "type": "error_recovery",
        "severity": "easy",
        "title": "Scan non-existent path",
        "prompt": "Scan a directory called target/nonexistent/.",
        "files": [],
        "expect": {"graceful_error": True},
    },
    {
        "id": "err-002",
        "type": "error_recovery",
        "severity": "easy",
        "title": "Read non-existent file",
        "prompt": "Read the file target/does_not_exist.py and tell me what's in it.",
        "files": [],
        "expect": {"graceful_error": True},
    },
    {
        "id": "err-003",
        "type": "error_recovery",
        "severity": "medium",
        "title": "Invalid rule ID",
        "prompt": "Explain what rule XXX999 means.",
        "files": [],
        "expect": {"graceful_error": True},
    },
    {
        "id": "err-004",
        "type": "error_recovery",
        "severity": "medium",
        "title": "Fix non-existent file",
        "prompt": "Fix the code issues in target/nonexistent_file.py.",
        "files": [],
        "expect": {"graceful_error": True},
    },
    {
        "id": "err-005",
        "type": "error_recovery",
        "severity": "hard",
        "title": "Mixed valid and invalid paths",
        "prompt": "Scan target/valid.py (which exists) and target/invalid.py (which doesn't). Report what happens.",
        "files": [("bad_python.py", "target/valid.py")],
        "expect": {"graceful_error": True, "scan_issues_gt": 0},
    },
]

# ===========================================================================
# Find scenario by ID
# ===========================================================================

ALL_SCENARIOS = SEC_BASE + STY_BASE + CPX_BASE + RPT_BASE + CMP_BASE + ERR_BASE

# Verify we have 50
if len(ALL_SCENARIOS) != 50:
    raise RuntimeError(f"Expected 50 scenarios, got {len(ALL_SCENARIOS)}")

SCENARIO_MAP = {s["id"]: s for s in ALL_SCENARIOS}


def get_scenario(scenario_id: str) -> dict | None:
    return SCENARIO_MAP.get(scenario_id)


def get_scenarios_by_type(scenario_type: str) -> list[dict]:
    return [s for s in ALL_SCENARIOS if s["type"] == scenario_type]


def get_scenarios_by_severity(severity: str) -> list[dict]:
    return [s for s in ALL_SCENARIOS if s["severity"] == severity]
