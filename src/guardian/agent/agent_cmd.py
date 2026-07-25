from __future__ import annotations
import sys
import typer
from guardian.agent.agent import run_agent
from guardian.chat.llm import check_llm_available, get_setup_guide


def agent(
    task: str = typer.Argument(..., help="Natural language task description for the agent"),
    max_steps: int = typer.Option(10, "--max-steps", "-s", help="Maximum number of tool-calling steps"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show detailed step trace"),
):
    """Run the AI agent with a natural language task (scan, fix, report, etc.)."""
    if not check_llm_available():
        typer.echo("❌ LLM not configured. Please set API key in .env")
        typer.echo("")
        typer.echo(get_setup_guide())
        raise typer.Exit(1)

    typer.echo("")
    typer.echo("🤖 QualiGuard Agent")
    typer.echo("━" * 40)
    typer.echo(f"  Task: {task}")
    typer.echo(f"  Max steps: {max_steps}")
    typer.echo("━" * 40)
    typer.echo("")

    result = run_agent(task, max_steps=max_steps, trace=True)

    answer = result["answer"]
    trace = result["trace"]

    # Print the steps if verbose
    if verbose and trace.steps:
        typer.echo("📋 Execution Trace:")
        typer.echo("─" * 40)
        for step in trace.steps:
            icon = "💬" if not step["tool_calls"] else "🔧"
            typer.echo(f"  Step {step['step']} {icon} ({step['duration_ms']}ms)")
            if step["content"]:
                typer.echo(f"     {step['content'][:120]}")
            for tc in step["tool_calls"]:
                typer.echo(f"     → {tc['name']}({_shorten_args(tc['arguments'])}) [{tc['duration_ms']}ms]")
        typer.echo("─" * 40)
        typer.echo("")

    # Print the final answer
    typer.echo("📝 Result:")
    typer.echo("─" * 40)
    typer.echo(answer)
    typer.echo("─" * 40)

    # Summary
    status = "✅" if trace.success else "⚠️"
    typer.echo(f"")
    typer.echo(f"  {status} Steps: {len(trace.steps)} | Tokens: {trace.total_tokens} | Duration: {_fmt_duration(trace.total_duration_ms)}")


def _shorten_args(args: str, max_len: int = 60) -> str:
    if len(args) <= max_len:
        return args
    return args[:max_len] + "..."


def _fmt_duration(ms: int) -> str:
    if ms < 1000:
        return f"{ms}ms"
    return f"{ms / 1000:.1f}s"
