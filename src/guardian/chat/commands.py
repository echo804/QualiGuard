from __future__ import annotations
import sys, os


def cmd_scan(args: str) -> str:
    """Run code analysis."""
    from guardian.core.session import Session
    from guardian.core.scheduler import Scheduler
    from guardian.checkers.static_analyzer import StaticAnalyzer
    from guardian.checkers.style_checker import StyleChecker
    from guardian.checkers.security_scanner import SecurityScanner
    from guardian.checkers.complexity import ComplexityAnalyzer
    from guardian.checkers.dependency import DependencyChecker
    from guardian.rules.engine import RuleEngine
    from guardian.rules.loader import load_rules
    from guardian.reporters.terminal import TerminalReporter

    target = args.strip() or os.getcwd()
    session = Session(target)
    rules = load_rules(session.config.rules)
    rule_engine = RuleEngine(rules)
    checkers = [
        StaticAnalyzer(rule_engine), StyleChecker(rule_engine),
        SecurityScanner(rule_engine), ComplexityAnalyzer(rule_engine),
        DependencyChecker(rule_engine),
    ]
    result = session.create_result()
    scheduler = Scheduler(checkers)
    scheduler.run(target, result)
    return TerminalReporter().generate(result)

def cmd_fix(args: str) -> str:
    """Auto-fix fixable issues."""
    from guardian.fixers.scheduler import FixScheduler
    from guardian.core.session import Session
    from guardian.core.scheduler import Scheduler

    target = args.strip() or os.getcwd()
    session = Session(target)
    checkers = []
    result = session.create_result()
    scheduler_obj = Scheduler(checkers)
    try:
        from guardian.checkers.static_analyzer import StaticAnalyzer
        from guardian.checkers.style_checker import StyleChecker
        checkers.extend([StaticAnalyzer(), StyleChecker()])
    except Exception:
        pass
    scheduler_obj = Scheduler(checkers)
    scheduler_obj.run(target, result)

    fixer = FixScheduler()
    fixed = fixer.fix_issues(result.issues)
    return f"Fixed {fixed}/{len(result.issues)} fixable issues."


def cmd_rules(args: str) -> str:
    """List rules."""
    from guardian.cli.rules_cmd import rules
    import io
    captured = io.StringIO()
    old = sys.stdout
    sys.stdout = captured
    try:
        rules(list_all=True)
    finally:
        sys.stdout = old
    return captured.getvalue()


def cmd_report(args: str) -> str:
    """Generate HTML report."""
    from guardian.core.session import Session
    from guardian.core.scheduler import Scheduler
    from guardian.reporters.html_reporter import HtmlReporter
    from guardian.checkers.static_analyzer import StaticAnalyzer
    from guardian.checkers.style_checker import StyleChecker
    from guardian.checkers.security_scanner import SecurityScanner
    from guardian.checkers.complexity import ComplexityAnalyzer
    from guardian.checkers.dependency import DependencyChecker
    from guardian.rules.engine import RuleEngine
    from guardian.rules.loader import load_rules

    target = args.strip() or os.getcwd()
    output_path = os.path.join(target, "qualiguard-report.html") if os.path.isdir(target) else "qualiguard-report.html"
    session = Session(target)
    rules = load_rules(session.config.rules)
    rule_engine = RuleEngine(rules)
    checkers = [
        StaticAnalyzer(rule_engine), StyleChecker(rule_engine),
        SecurityScanner(rule_engine), ComplexityAnalyzer(rule_engine),
        DependencyChecker(rule_engine),
    ]
    result = session.create_result()
    scheduler = Scheduler(checkers)
    scheduler.run(target, result)
    reporter = HtmlReporter()
    reporter.generate(result, output_path)
    formatted_path = output_path.replace("\\", "/")
    return f"HTML report generated: {formatted_path}"


def cmd_read(args: str) -> str:
    """Read a file and return its contents."""
    path = args.strip()
    if not path:
        return "  Usage: /read <filepath>  - Read and display file contents"
    abs_path = os.path.abspath(path)
    if not os.path.exists(abs_path):
        return f"  File not found: {abs_path}"
    try:
        with open(abs_path, encoding="utf-8", errors="replace") as f:
            content = f.read()
        lines = content.count("\n") + 1
        header = f"  --- {abs_path} ({lines} lines) ---"
        return header + "\n" + content + "\n" + "  --- end ---"
    except Exception as e:
        return f"  Error reading file: {e}"


COMMANDS = {
    "/scan": cmd_scan,
    "/fix": cmd_fix,
    "/rules": cmd_rules,
    "/report": cmd_report,
    "/read": cmd_read,
    "/cat": cmd_read,
    "/help": lambda _: """
  /scan <path>   执行代码质量分析
  /fix  <path>   自动修复可修复的问题
  /report <path> 生成 HTML 报告
  /rules         列出所有规则
  /read <file>   读取文件内容并交给 AI 分析
  /cat  <file>   同上（/read 的别名）
  /help          显示此帮助
  /clear         清除聊天历史
  /exit          退出聊天
""",
    "/clear": lambda _: "__CLEAR__",
    "/exit": lambda _: "__EXIT__",
    "/quit": lambda _: "__EXIT__",
}
