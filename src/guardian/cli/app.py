from __future__ import annotations
import sys
import typer
from guardian.cli.scan_cmd import scan
from guardian.cli.fix_cmd import fix
from guardian.cli.rules_cmd import rules
from guardian.cli.init_cmd import init
from guardian.cli.chat_cmd import chat
from guardian.agent.agent_cmd import agent
from guardian.eval.eval_cmd import eval_command

import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Fix Windows console encoding
if sys.platform == "win32" and hasattr(sys.stdout, "buffer"):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

app = typer.Typer(
    name="qg",
    help="QualiGuard - AI 驱动的代码质量分析 CLI 工具",
    no_args_is_help=True,
)

app.command(name="scan", help="扫描文件或目录，检测代码质量问题")(scan)
app.command(name="fix", help="自动修复可修复的代码问题")(fix)
app.command(name="rules", help="查看和管理规则列表")(rules)
app.command(name="init", help="生成 .guardian.yaml 配置文件")(init)
app.command(name="eval", help="Run agent evaluation benchmark")(eval_command)
app.command(name="agent", help="Run AI agent with a natural language task (scan, fix, report, etc.)")(agent)
app.command(name="chat", help="启动交互式对话模式（类似 Claude Code）")(chat)


@app.callback()
def main():
    pass