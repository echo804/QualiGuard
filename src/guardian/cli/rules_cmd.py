from __future__ import annotations
import typer


def rules(
    list_all: bool = typer.Option(False, "--list", "-l", help="列出所有可用规则"),
):
    """查看和管理规则列表。"""
    typer.echo("QualiGuard 规则列表")
    typer.echo("=" * 40)
    typer.echo("  STA001 - long-function        - 警告 - 函数过长，建议拆分")
    typer.echo("  CPX001 - high-complexity       - 警告 - 圈复杂度过高")
    typer.echo("  SEC001 - hardcoded-password    - 错误 - 硬编码密码")
    typer.echo("  SEC002 - hardcoded-api-key     - 错误 - 硬编码 API Key")
    typer.echo("  SEC004 - dangerous-eval        - 错误 - 使用 eval() 可能导致代码注入")
    typer.echo("  DEP001 - vulnerable-dependency - 警告 - 已知漏洞依赖")
