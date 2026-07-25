"""CLI command: qg eval"""

from __future__ import annotations
import sys
import typer
from pathlib import Path

from guardian.eval.scenarios import (
    ALL_SCENARIOS,
    get_scenarios_by_type,
    get_scenarios_by_severity,
)
from guardian.eval.runner import run_scenarios
from guardian.eval.metrics import compute_metrics
from guardian.eval.report import generate_report
from guardian.chat.llm import check_llm_available, get_setup_guide


def eval_command(
    count: int = typer.Option(50, "--scenarios", "-n", help="Number of scenarios to run (default: all 50)"),
    scenario_type: str = typer.Option(None, "--type", "-t", help="Filter by type: security/style/complexity/report/comprehensive/error_recovery"),
    severity: str = typer.Option(None, "--severity", "-s", help="Filter by severity: easy/medium/hard"),
    max_steps: int = typer.Option(10, "--max-steps", "-m", help="Max agent steps per scenario"),
    output: str = typer.Option(None, "--output", "-o", help="Save report to file"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show detailed per-scenario results"),
):
    """Run agent evaluation and generate a performance report."""
    if not check_llm_available():
        typer.echo("❌ LLM not configured. Please set API key in .env")
        typer.echo("")
        typer.echo(get_setup_guide())
        raise typer.Exit(1)

    # Filter scenarios
    scenarios = ALL_SCENARIOS
    if scenario_type:
        scenarios = get_scenarios_by_type(scenario_type)
    if severity:
        scenarios = get_scenarios_by_severity(severity)
    scenarios = scenarios[:count]

    typer.echo("")
    typer.echo("🧪 QualiGuard Agent 评测")
    typer.echo("=" * 48)
    typer.echo(f"  场景数: {len(scenarios)}")
    typer.echo(f"  最大步数: {max_steps}")
    typer.echo(f"  输出: {output or '终端'}")
    typer.echo("=" * 48)
    typer.echo("")

    # Progress callback
    def progress(scenario_id: str, index: int, total: int):
        typer.echo(f"  [{index}/{total}] Running {scenario_id}...")
        typer.echo()

    # Run
    results = run_scenarios(scenarios, max_steps=max_steps, progress_callback=progress)

    # Compute metrics
    from guardian.chat.llm import _find_config
    _, _, model_name = _find_config()
    metrics = compute_metrics(results)
    report = generate_report(metrics, model_name=model_name or "unknown")

    # Output
    if output:
        out_path = Path(output)
        out_path.write_text(report, encoding="utf-8")
        typer.echo(f"✅ 报告已保存: {out_path.resolve()}")
    else:
        typer.echo(report)

    # Summary line
    typer.echo(f"📊 结果: {metrics.passed}/{metrics.total_scenarios} 通过 ({metrics.pass_rate:.1f}%)")
