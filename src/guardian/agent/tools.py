from __future__ import annotations
import os
import re
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Callable


@dataclass
class Tool:
    """A callable tool with an OpenAI-compatible function schema."""
    name: str
    description: str
    parameters: dict
    fn: Callable[..., str]

    @property
    def schema(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters,
            },
        }

    def __call__(self, **kwargs: str) -> str:
        try:
            return self.fn(**kwargs)
        except Exception as exc:
            return f"[ToolError] {self.name} failed: {exc}"


# ===================================================================
# Tool implementations
# ===================================================================

def _scan_code(path: str = ".", rules: str = "") -> str:
    """Scan code and return issue summary."""
    from guardian.core.session import Session
    from guardian.core.scheduler import Scheduler
    from guardian.checkers.static_analyzer import StaticAnalyzer
    from guardian.checkers.style_checker import StyleChecker
    from guardian.checkers.security_scanner import SecurityScanner
    from guardian.checkers.complexity import ComplexityAnalyzer
    from guardian.checkers.dependency import DependencyChecker
    from guardian.rules.engine import RuleEngine
    from guardian.rules.loader import load_rules

    session = Session(path)
    rules_list = load_rules(session.config.rules)

    if rules:
        filtered = [r for r in rules_list if rules.lower() in r.id.lower()]
        if not filtered:
            return f"[Warn] No matching rules for '{rules}', using all rules"
        rule_engine = RuleEngine(filtered)
    else:
        rule_engine = RuleEngine(rules_list)

    checkers = [
        StaticAnalyzer(rule_engine),
        StyleChecker(rule_engine),
        SecurityScanner(rule_engine),
        ComplexityAnalyzer(rule_engine),
        DependencyChecker(rule_engine),
    ]

    result = session.create_result()
    scheduler = Scheduler(checkers)
    scheduler.run(path, result)

    lines = [f"Target: {path}", f"Files: {result.scanned_files}/{result.total_files}"]
    lines.append(f"Issues found: {len(result.issues)}")
    lines.append(f"  ERROR: {result.error_count}")
    lines.append(f"  WARN:  {result.warning_count}")
    lines.append(f"  INFO:  {result.info_count}")
    if result.issues:
        lines.append("")
        for iss in result.issues[:20]:
            lines.append(f"  [{iss.severity.value.upper()}] {iss.rule_id}  {iss.file_path}:{iss.line}")
            lines.append(f"         {iss.message}")
        if len(result.issues) > 20:
            lines.append(f"  ... and {len(result.issues) - 20} more issues")
    return "\n".join(lines)


def _fix_code(path: str = ".") -> str:
    """Auto-fix fixable code issues."""
    from guardian.core.session import Session
    from guardian.core.scheduler import Scheduler
    from guardian.checkers.static_analyzer import StaticAnalyzer
    from guardian.checkers.style_checker import StyleChecker
    from guardian.checkers.security_scanner import SecurityScanner
    from guardian.checkers.complexity import ComplexityAnalyzer
    from guardian.checkers.dependency import DependencyChecker
    from guardian.rules.engine import RuleEngine
    from guardian.rules.loader import load_rules
    from guardian.fixers.scheduler import FixScheduler

    session = Session(path)
    rules_list = load_rules(session.config.rules)
    rule_engine = RuleEngine(rules_list)

    checkers = [
        StaticAnalyzer(rule_engine),
        StyleChecker(rule_engine),
        SecurityScanner(rule_engine),
        ComplexityAnalyzer(rule_engine),
        DependencyChecker(rule_engine),
    ]

    result = session.create_result()
    scheduler_obj = Scheduler(checkers)
    scheduler_obj.run(path, result)

    if not result.issues:
        return "No issues found, nothing to fix."

    fix_scheduler = FixScheduler()
    fixable = [i for i in result.issues if any(f.can_fix(i) for f in fix_scheduler.fixers)]

    if not fixable:
        return f"Found {len(result.issues)} issues, but none can be auto-fixed."

    fixed = fix_scheduler.fix_issues(fixable)
    return (
        f"Target: {path}\n"
        f"Fixable: {len(fixable)} | Fixed: {fixed} | Failed: {len(fixable) - fixed}\n"
        f"Cannot auto-fix: {len(result.issues) - len(fixable)}"
    )


def _read_file(path: str = "") -> str:
    """Read file content."""
    resolved = Path(path).resolve()
    if not resolved.is_file():
        return f"[Error] File not found: {path}"
    content = resolved.read_text(encoding="utf-8", errors="replace")
    lines = content.splitlines()
    return f"--- {resolved} ({len(lines)} lines) ---\n" + content + "\n--- end ---"


def _search_code(pattern: str = "", path: str = ".") -> str:
    """Search code for a regex pattern."""
    import glob as glob_mod

    root = Path(path).resolve()
    results = []
    EXTENSIONS = {
        ".py", ".js", ".ts", ".go", ".rs", ".java",
        ".c", ".h", ".cpp", ".hpp",
        ".yaml", ".yml", ".json", ".toml",
        ".md", ".txt", ".cfg", ".ini", ".env",
    }

    for file_path in glob_mod.iglob(str(root / "**"), recursive=True):
        p = Path(file_path)
        if not p.is_file():
            continue
        if p.suffix not in EXTENSIONS:
            continue
        try:
            text = p.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        for lineno, line in enumerate(text.splitlines(), 1):
            try:
                if re.search(pattern, line, re.IGNORECASE):
                    rel = p.relative_to(root)
                    results.append(f"  {rel}:{lineno}  {line.strip()[:120]}")
                    if len(results) >= 50:
                        break
            except re.error:
                return f"[Error] Invalid regex pattern: {pattern}"
        if len(results) >= 50:
            break

    if not results:
        return f"No matches for '{pattern}'."
    return f"Pattern: {pattern}\nMatches ({len(results)}):\n" + "\n".join(results)


def _generate_report(format: str = "terminal", output_path: str = "") -> str:
    """Run full scan and generate report."""
    from guardian.core.session import Session
    from guardian.core.scheduler import Scheduler
    from guardian.checkers.static_analyzer import StaticAnalyzer
    from guardian.checkers.style_checker import StyleChecker
    from guardian.checkers.security_scanner import SecurityScanner
    from guardian.checkers.complexity import ComplexityAnalyzer
    from guardian.checkers.dependency import DependencyChecker
    from guardian.rules.engine import RuleEngine
    from guardian.rules.loader import load_rules
    from guardian.reporters import REPORTER_MAP

    session = Session(".")
    rules_list = load_rules(session.config.rules)
    rule_engine = RuleEngine(rules_list)

    checkers = [
        StaticAnalyzer(rule_engine),
        StyleChecker(rule_engine),
        SecurityScanner(rule_engine),
        ComplexityAnalyzer(rule_engine),
        DependencyChecker(rule_engine),
    ]

    result = session.create_result()
    scheduler = Scheduler(checkers)
    scheduler.run(".", result)

    fmt = format.lower()
    reporter_cls = REPORTER_MAP.get(fmt)
    if reporter_cls is None:
        supported = ", ".join(REPORTER_MAP.keys())
        return f"[Error] Unsupported format: {format}. Supported: {supported}"

    reporter = reporter_cls()
    out = Path(output_path) if output_path else None
    text = reporter.generate(result, str(out) if out else None)

    if out:
        return f"Report saved: {out.resolve()}"
    return text


def _explain_rule(rule_id: str = "") -> str:
    """Look up rule details."""
    from guardian.rules.loader import load_rules
    from guardian.config.loader import load_config

    config = load_config(None)
    rules = load_rules(config.rules)

    for rule in rules:
        rid = rule.get("id", "")
        if rid.upper() == rule_id.upper():
            lines = [
                f"Rule: {rid}",
                f"Severity: {rule.get('severity', 'unknown').upper()}",
                f"Description: {rule.get('description', '')}",
            ]
            msg = rule.get("message") or rule.get("message_template") or ""
            if msg:
                lines.append(f"Message: {msg}")
            return "\n".join(lines)
    return f"Rule not found: {rule_id}"


# ===================================================================
# Tool registry
# ===================================================================

ALL_TOOLS: list[Tool] = [
    Tool(
        name="scan_code",
        description="Run code quality scan on a file or directory. Checks security, style, complexity, etc.",
        parameters={
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "File or directory path to scan, defaults to current dir",
                    "default": ".",
                },
                "rules": {
                    "type": "string",
                    "description": "Optional rule filter prefix, e.g. SEC, STY, CPX. Empty = all rules",
                    "default": "",
                },
            },
        },
        fn=_scan_code,
    ),
    Tool(
        name="fix_code",
        description="Auto-fix fixable code issues in a file or directory (style, imports, etc.).",
        parameters={
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "File or directory path to fix, defaults to current dir",
                    "default": ".",
                },
            },
        },
        fn=_fix_code,
    ),
    Tool(
        name="read_file",
        description="Read a file's content for code analysis.",
        parameters={
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Path to the file to read",
                },
            },
            "required": ["path"],
        },
        fn=_read_file,
    ),
    Tool(
        name="search_code",
        description="Search the codebase with a regex pattern to find specific code.",
        parameters={
            "type": "object",
            "properties": {
                "pattern": {
                    "type": "string",
                    "description": "Regex pattern to search for",
                },
                "path": {
                    "type": "string",
                    "description": "Root directory to search, defaults to current dir",
                    "default": ".",
                },
            },
            "required": ["pattern"],
        },
        fn=_search_code,
    ),
    Tool(
        name="generate_report",
        description="Run a full scan and generate a quality report in the specified format.",
        parameters={
            "type": "object",
            "properties": {
                "format": {
                    "type": "string",
                    "description": "Report format: terminal, json, html, markdown, sarif",
                    "enum": ["terminal", "json", "html", "markdown", "sarif"],
                    "default": "terminal",
                },
                "output_path": {
                    "type": "string",
                    "description": "Output file path (optional). Prints to terminal if empty",
                    "default": "",
                },
            },
        },
        fn=_generate_report,
    ),
    Tool(
        name="explain_rule",
        description="Show detailed explanation of a code quality rule.",
        parameters={
            "type": "object",
            "properties": {
                "rule_id": {
                    "type": "string",
                    "description": "Rule ID, e.g. SEC001, CPX001, STY001",
                },
            },
            "required": ["rule_id"],
        },
        fn=_explain_rule,
    ),
]


def get_tool_schemas() -> list[dict]:
    """Return all tool schemas in OpenAI-compatible format."""
    return [t.schema for t in ALL_TOOLS]


def get_tool_by_name(name: str) -> Tool | None:
    """Look up a tool by name."""
    for t in ALL_TOOLS:
        if t.name == name:
            return t
    return None


def dispatch_tool_call(tool_name: str, arguments: str | dict) -> str:
    """Execute a tool call and return the result string."""
    tool = get_tool_by_name(tool_name)
    if tool is None:
        return f"[ToolError] Unknown tool: {tool_name}"
    if isinstance(arguments, str):
        try:
            kwargs = json.loads(arguments)
        except json.JSONDecodeError:
            return f"[ToolError] Failed to parse arguments: {arguments}"
    else:
        kwargs = arguments
    return tool(**kwargs)
