from __future__ import annotations
import typer
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


def scan(
    target: str = typer.Argument(".", help="要扫描的文件或目录路径"),
    config: str = typer.Option(None, "--config", "-c", help="配置文件路径 (.guardian.yaml)"),
    output_format: str = typer.Option("terminal", "--format", "-f", help="输出格式: terminal / json / html / markdown / sarif"),
    output: str = typer.Option(None, "--output", "-o", help="输出文件路径"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="输出详细日志"),
):
    """扫描文件或目录，检测代码质量问题。"""
    session = Session(target, config)
    if output_format:
        session.config.output_format = output_format
    if output:
        session.config.output_path = output
    session.config.verbose = verbose

    rules = load_rules(session.config.rules)
    rule_engine = RuleEngine(rules)

    checkers = [
        StaticAnalyzer(rule_engine),
        StyleChecker(rule_engine),
        SecurityScanner(rule_engine),
        ComplexityAnalyzer(rule_engine),
        DependencyChecker(rule_engine),
    ]

    result = session.create_result()
    scheduler = Scheduler(checkers)
    scheduler.run(target, result)

    # Select reporter based on format
    reporter_cls = REPORTER_MAP.get(output_format)
    if reporter_cls is None:
        typer.echo(f"未知的输出格式: {output_format}，使用 terminal", err=True)
        reporter_cls = REPORTER_MAP["terminal"]

    reporter = reporter_cls()
    report_text = reporter.generate(result, output)
    if not output:
        print(report_text)