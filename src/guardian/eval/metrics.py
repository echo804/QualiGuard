"""Metrics calculation for evaluation results."""

from __future__ import annotations
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from typing import Any

from guardian.eval.runner import ScenarioResult


@dataclass
class EvalMetrics:
    """Aggregated evaluation metrics."""
    # Overall
    total_scenarios: int = 0
    passed: int = 0
    failed: int = 0
    pass_rate: float = 0.0

    # By type
    by_type: dict[str, dict[str, Any]] = field(default_factory=dict)

    # By severity
    by_severity: dict[str, dict[str, Any]] = field(default_factory=dict)

    # Performance
    avg_steps: float = 0.0
    avg_tool_calls: float = 0.0
    avg_tokens: float = 0.0
    avg_duration_ms: float = 0.0

    # Tool usage
    tool_usage: dict[str, int] = field(default_factory=dict)

    # Failure analysis
    failure_reasons: Counter = field(default_factory=Counter)
    failed_scenarios: list[str] = field(default_factory=list)

    # Raw results
    results: list[ScenarioResult] = field(default_factory=list)


def compute_metrics(results: list[ScenarioResult]) -> EvalMetrics:
    """Compute aggregated metrics from scenario results."""
    metrics = EvalMetrics()
    metrics.results = results
    metrics.total_scenarios = len(results)
    metrics.passed = sum(1 for r in results if r.passed)
    metrics.failed = metrics.total_scenarios - metrics.passed
    metrics.pass_rate = (metrics.passed / metrics.total_scenarios * 100) if metrics.total_scenarios > 0 else 0.0

    # By type
    type_groups = defaultdict(list)
    for r in results:
        type_groups[r.scenario_type].append(r)

    for t, group in sorted(type_groups.items()):
        passed = sum(1 for r in group if r.passed)
        total = len(group)
        metrics.by_type[t] = {
            "total": total,
            "passed": passed,
            "failed": total - passed,
            "pass_rate": passed / total * 100 if total > 0 else 0.0,
            "avg_steps": sum(r.steps_count for r in group) / total if total > 0 else 0.0,
            "avg_tokens": sum(r.total_tokens for r in group) / total if total > 0 else 0.0,
            "avg_duration_ms": sum(r.duration_ms for r in group) / total if total > 0 else 0.0,
        }

    # By severity
    sev_groups = defaultdict(list)
    for r in results:
        sev_groups[r.severity].append(r)

    for s, group in sorted(sev_groups.items()):
        passed = sum(1 for r in group if r.passed)
        total = len(group)
        metrics.by_severity[s] = {
            "total": total,
            "passed": passed,
            "failed": total - passed,
            "pass_rate": passed / total * 100 if total > 0 else 0.0,
        }

    # Performance averages
    if results:
        metrics.avg_steps = sum(r.steps_count for r in results) / len(results)
        metrics.avg_tool_calls = sum(r.tool_calls_count for r in results) / len(results)
        metrics.avg_tokens = sum(r.total_tokens for r in results) / len(results)
        metrics.avg_duration_ms = sum(r.duration_ms for r in results) / len(results)

    # Tool usage
    tool_counter: Counter = Counter()
    for r in results:
        pass  # tool usage details stored in each result

    # Failure analysis
    failure_counter: Counter = Counter()
    failed_ids: list[str] = []
    for r in results:
        if not r.passed:
            failed_ids.append(f"{r.scenario_id}: {r.title}")
            for err in r.errors:
                failure_counter[err] += 1

    metrics.failure_reasons = failure_counter
    metrics.failed_scenarios = failed_ids

    return metrics
