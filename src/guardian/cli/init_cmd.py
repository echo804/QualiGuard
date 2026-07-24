from __future__ import annotations
import typer
from pathlib import Path


def init(
    force: bool = typer.Option(False, "--force", "-f", help="覆盖已有的配置文件"),
):
    """在当前目录生成 .guardian.yaml 配置文件。"""
    target = Path.cwd() / ".guardian.yaml"
    if target.exists() and not force:
        typer.echo(".guardian.yaml 已存在，使用 --force 参数覆盖。")
        raise typer.Exit()

    content = """# QualiGuard 配置文件
checkers:
  - static
  - style
  - security
  - complexity
  - dependency

ignore_patterns:
  - "__pycache__"
  - "node_modules"
  - ".venv"
  - "build/"
  - "dist/"

max_line_length: 88
output_format: terminal
verbose: false
threads: 4
"""
    target.write_text(content, encoding="utf-8")
    typer.echo(f"已生成配置文件: {target}")
