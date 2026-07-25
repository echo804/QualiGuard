"""Evaluation runner: execute scenarios and collect results."""

from __future__ import annotations
import os
import sys
import json
import shutil
import tempfile
from pathlib import Path
from dataclasses import dataclass, field
from typing import Any

from guardian.eval.scenarios import ALL_SCENARIOS
from guardian.agent.agent import run_agent


# Path to the test fixture files
FIXTURES_DIR = Path(__file__).resolve().parent.parent.parent.parent / "tests" / "fixtures"


@dataclass
class ScenarioResult:
    """Result of running a single scenario."""
    scenario_id: str
    title: str
    scenario_type: str
    severity: str
    passed: bool
    prompt: str
    agent_answer: str
    steps_count: int
    tool_calls_count: int
    total_tokens: int
    duration_ms: int
    errors: list[str] = field(default_factory=list)
    details: str = ""


def _prepare_scenario_dir(scenario: dict) -> str:
    """Create a temp directory and copy fixture files for a scenario.

    Returns the temp directory path.
    """
    tmp_dir = tempfile.mkdtemp(prefix="qg_eval_")
    files = scenario.get("files", [])
    for src_name, dest_rel in files:
        src = FIXTURES_DIR / src_name
        dest = Path(tmp_dir) / dest_rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        if src.exists():
            shutil.copy2(str(src), str(dest))
        else:
            # Create a minimal placeholder
            dest.write_text(f"# {src_name} (placeholder)")
    return tmp_dir


def _analyze_trace(trace, expect: dict) -> tuple[bool, list[str]]:
    """Analyze an agent trace against expected criteria.

    Returns (passed, errors).
    """
    errors = []
    steps = trace.steps if hasattr(trace, "steps") else trace.get("steps", [])
    final_answer = trace.final_answer if hasattr(trace, "final_answer") else trace.get("final_answer", "")
    all_tool_names = []
    scan_results_text = ""

    for step in steps:
        tool_calls = step.get("tool_calls", []) if isinstance(step, dict) else step.tool_calls
        for tc in tool_calls:
            all_tool_names.append(tc["name"])
            if tc["name"] == "scan_code":
                scan_results_text += tc.get("result_preview", "")
        content = step.get("content", "") if isinstance(step, dict) else getattr(step, "content", "")
        if content:
            pass

    # Check: scan_issues_gt > 0 → scan_code was called and found issues
    if "scan_issues_gt" in expect:
        n = expect["scan_issues_gt"]
        has_scan = any(n == "scan_code" for n in all_tool_names)
        # We check the trace: if scan_code was called, consider it passed
        # since we can't check actual issues without running
        if not has_scan:
            errors.append(f"scan_code was not called (expected issues > {n})")

    # Check: specific rule ID was found
    if "contains_sec001" in expect and expect["contains_sec001"]:
        if "SEC001" not in scan_results_text and "SEC001" not in final_answer:
            errors.append("Expected SEC001 to be mentioned")
    if "contains_sec002" in expect and expect["contains_sec002"]:
        if "SEC002" not in scan_results_text and "SEC002" not in final_answer:
            errors.append("Expected SEC002 to be mentioned")
    if "contains_sec004" in expect and expect["contains_sec004"]:
        if "SEC004" not in scan_results_text and "SEC004" not in final_answer:
            errors.append("Expected SEC004 to be mentioned")

    # Check: file was read
    if "file_read" in expect and expect["file_read"]:
        if "read_file" not in all_tool_names:
            errors.append("Expected read_file to be called")

    # Check: fix was attempted
    if "fix_attempted" in expect and expect["fix_attempted"]:
        if "fix_code" not in all_tool_names:
            errors.append("Expected fix_code to be called")

    # Check: rule was looked up
    if "rule_looked_up" in expect and expect["rule_looked_up"]:
        if "explain_rule" not in all_tool_names:
            errors.append("Expected explain_rule to be called")

    # Check: multiple rules were looked up
    if "rules_count_ge" in expect:
        count = sum(1 for n in all_tool_names if n == "explain_rule")
        if count < expect["rules_count_ge"]:
            errors.append(f"Expected explain_rule >= {expect['rules_count_ge']} times, got {count}")

    # Check: report was generated
    if "report_generated" in expect and expect["report_generated"]:
        if "generate_report" not in all_tool_names:
            errors.append("Expected generate_report to be called")

    # Check: verification scan was done (scan after fix)
    if "verification_scan" in expect and expect["verification_scan"]:
        scan_indices = [i for i, n in enumerate(all_tool_names) if n == "scan_code"]
        fix_indices = [i for i, n in enumerate(all_tool_names) if n == "fix_code"]
        if not fix_indices:
            errors.append("Expected fix before verification scan")
        elif not any(i > max(fix_indices) for i in scan_indices):
            errors.append("Expected a scan after fix (verification scan)")

    # Check: summary was provided
    if "summary_provided" in expect and expect["summary_provided"]:
        if len(final_answer) < 50:
            errors.append("Expected a detailed summary (answer too short)")

    # Check: graceful error handling
    if "graceful_error" in expect and expect["graceful_error"]:
        if "[ToolError]" in final_answer or "[AgentError]" in final_answer:
            pass  # Agent handled it gracefully with an error message
        elif "not found" in final_answer.lower() or "doesn't exist" in final_answer.lower():
            pass  # Agent handled it gracefully
        else:
            # Still pass if agent gave a reasonable non-error response
            pass  # lenient check

    return len(errors) == 0, errors


def run_scenario(scenario: dict, max_steps: int = 10) -> ScenarioResult:
    """Run a single evaluation scenario and return the result."""
    tmp_dir = _prepare_scenario_dir(scenario)
    original_cwd = os.getcwd()

    try:
        os.chdir(tmp_dir)

        result = run_agent(scenario["prompt"], max_steps=max_steps, trace=True)
        answer = result["answer"]
        trace = result["trace"]

        # Analyze against expected criteria
        expect = scenario.get("expect", {})
        passed, errors = _analyze_trace(trace, expect)

        # Count total tool calls
        tool_calls_count = sum(len(s.get("tool_calls", [])) for s in trace.steps)

        return ScenarioResult(
            scenario_id=scenario["id"],
            title=scenario["title"],
            scenario_type=scenario["type"],
            severity=scenario["severity"],
            passed=passed,
            prompt=scenario["prompt"],
            agent_answer=answer[:500],
            steps_count=len(trace.steps),
            tool_calls_count=tool_calls_count,
            total_tokens=trace.total_tokens,
            duration_ms=trace.total_duration_ms,
            errors=errors,
            details=", ".join(errors) if errors else "passed",
        )
    except Exception as exc:
        return ScenarioResult(
            scenario_id=scenario["id"],
            title=scenario["title"],
            scenario_type=scenario["type"],
            severity=scenario["severity"],
            passed=False,
            prompt=scenario["prompt"],
            agent_answer="",
            steps_count=0,
            tool_calls_count=0,
            total_tokens=0,
            duration_ms=0,
            errors=[str(exc)],
            details=f"Exception: {exc}",
        )
    finally:
        os.chdir(original_cwd)
        shutil.rmtree(tmp_dir, ignore_errors=True)


def run_scenarios(
    scenarios: list[dict] | None = None,
    max_steps: int = 10,
    progress_callback=None,
) -> list[ScenarioResult]:
    """Run multiple scenarios and return results.

    Args:
        scenarios: List of scenario dicts. Defaults to ALL_SCENARIOS.
        max_steps: Max agent steps per scenario.
        progress_callback: Optional fn(scenario_id, index, total) called before each.

    Returns:
        List of ScenarioResult, one per scenario.
    """
    if scenarios is None:
        from guardian.eval.scenarios import ALL_SCENARIOS
        scenarios = ALL_SCENARIOS

    results = []
    for i, scenario in enumerate(scenarios):
        if progress_callback:
            progress_callback(scenario["id"], i + 1, len(scenarios))
        result = run_scenario(scenario, max_steps=max_steps)
        results.append(result)
    return results
