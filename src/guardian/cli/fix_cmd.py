from __future__ import annotations
import sys
import typer
from guardian.core.session import Session
from guardian.core.scheduler import Scheduler
from guardian.core.models import Severity
from guardian.checkers.static_analyzer import StaticAnalyzer
from guardian.checkers.style_checker import StyleChecker
from guardian.checkers.security_scanner import SecurityScanner
from guardian.checkers.complexity import ComplexityAnalyzer
from guardian.checkers.dependency import DependencyChecker
from guardian.rules.engine import RuleEngine
from guardian.rules.loader import load_rules
from guardian.reporters import REPORTER_MAP
from guardian.fixers.scheduler import FixScheduler


def fix(
    target: str = typer.Argument(".", help="要修复的文件或目录路径"),
    config: str = typer.Option(None, "--config", "-c", help="配置文件路径"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="输出详细日志"),
    yes: bool = typer.Option(False, "--yes", "-y", help="跳过确认，直接执行修复"),
):
    """自动修复可修复的代码问题（交互式确认）。"""

    # ── 1. 执行扫描 ──
    session = Session(target, config)
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
    scheduler_obj = Scheduler(checkers)
    scheduler_obj.run(target, result)

    if not result.issues:
        typer.echo("\\n✅ 未发现需要修复的问题，代码质量良好！")
        raise typer.Exit()

    # ── 2. 分类：可修复 vs 不可修复 ──
    fix_scheduler = FixScheduler()
    fixable = []
    unfixable = []
    for issue in result.issues:
        can_fix = any(fixer.can_fix(issue) for fixer in fix_scheduler.fixers)
        if can_fix:
            fixable.append(issue)
        else:
            unfixable.append(issue)

    sev_label = {"error": "ERROR", "warning": "WARN", "info": "INFO"}

    # ── 3. 展示可修复的问题 ──
    typer.echo("\\n" + "=" * 56)
    typer.echo("  QualiGuard 自动修复")
    typer.echo("=" * 56)
    typer.echo(f"  扫描目标: {target}")
    typer.echo(f"  发现 {len(result.issues)} 个问题")
    typer.echo(f"  ├─ 可修复:   {len(fixable)}")
    typer.echo(f"  └─ 需手动处理: {len(unfixable)}")
    typer.echo("=" * 56)

    if fixable:
        typer.echo("\\n📋 可修复的问题：")
        typer.echo("-" * 56)
        for i, issue in enumerate(fixable, 1):
            label = sev_label.get(issue.severity.value, "INFO")
            typer.echo(f"  {i}. [{label}] {issue.rule_id}")
            typer.echo(f"     {issue.message}")
            typer.echo(f"     位置: {issue.file_path}:{issue.line}")
            typer.echo()

    if unfixable:
        typer.echo("\\n⚠️  需手动处理的问题（自动修复不支持）：")
        typer.echo("-" * 56)
        for i, issue in enumerate(unfixable, 1):
            label = sev_label.get(issue.severity.value, "INFO")
            typer.echo(f"  {i}. [{label}] {issue.rule_id}")
            typer.echo(f"     {issue.message}")
            typer.echo(f"     位置: {issue.file_path}:{issue.line}")
            typer.echo()

    # ── 4. 询问用户是否执行修复 ──
    if not fixable:
        typer.echo("没有可自动修复的问题。")
        raise typer.Exit()

    if not yes:
        typer.echo("-" * 56)
        confirm = typer.confirm("是否执行自动修复？", default=False)
        if not confirm:
            typer.echo("已取消修复。")
            raise typer.Exit()

    # ── 5. 执行修复 ──
    typer.echo("\\n🔧 正在执行自动修复...")
    fixed_count = fix_scheduler.fix_issues(fixable)

    typer.echo("\\n" + "=" * 56)
    typer.echo("  修复结果")
    typer.echo("=" * 56)
    typer.echo(f"  ✅ 已修复:  {fixed_count}/{len(fixable)}")
    typer.echo(f"  ❌ 失败:    {len(fixable) - fixed_count}")
    typer.echo(f"  ⚠️  需手动:  {len(unfixable)}")
    typer.echo("=" * 56)
    typer.echo("\\n请重新扫描以确认修复效果: qg scan " + target)