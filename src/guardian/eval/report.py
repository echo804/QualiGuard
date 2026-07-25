"""Generate evaluation report from metrics."""

from __future__ import annotations
from datetime import datetime
from guardian.eval.metrics import EvalMetrics


def generate_report(metrics: EvalMetrics, model_name: str = "unknown") -> str:
    """Generate a Markdown evaluation report."""
    lines = []
    _add = lines.append

    _add("# QualiGuard Agent 评测报告")
    _add("")
    _add(f"- **日期**: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    _add(f"- **模型**: {model_name}")
    _add(f"- **场景总数**: {metrics.total_scenarios}")
    _add("")

    # ═══════════════════════════════════════════
    # Section 1: Overall
    # ═══════════════════════════════════════════
    _add("## 一、总体指标")
    _add("")
    _add("| 指标 | 数值 |")
    _add("|------|------|")
    _add(f"| 测试场景数 | {metrics.total_scenarios} |")
    _add(f"| 通过 | {metrics.passed} |")
    _add(f"| 失败 | {metrics.failed} |")
    _add(f"| **通过率** | **{metrics.pass_rate:.1f}%** |")
    _add(f"| 平均步骤数 | {metrics.avg_steps:.1f} |")
    _add(f"| 平均工具调用 | {metrics.avg_tool_calls:.1f} |")
    _add(f"| 平均 Token 消耗 | {metrics.avg_tokens:.0f} |")
    _add(f"| 平均耗时 | {metrics.avg_duration_ms:.0f}ms |")
    _add("")

    # ═══════════════════════════════════════════
    # Section 2: By Type
    # ═══════════════════════════════════════════
    _add("## 二、按场景类型分析")
    _add("")
    _add("| 类型 | 总数 | 通过 | 失败 | 通过率 | 平均步数 | 平均 Token | 平均耗时 |")
    _add("|------|------|------|------|--------|----------|------------|----------|")
    for t, info in sorted(metrics.by_type.items()):
        _add(
            f"| {t} | {info['total']} | {info['passed']} | {info['failed']} | "
            f"{info['pass_rate']:.1f}% | {info['avg_steps']:.1f} | "
            f"{info['avg_tokens']:.0f} | {info['avg_duration_ms']:.0f}ms |"
        )
    _add("")

    # ═══════════════════════════════════════════
    # Section 3: By Severity
    # ═══════════════════════════════════════════
    _add("## 三、按难度分析")
    _add("")
    _add("| 难度 | 总数 | 通过 | 失败 | 通过率 |")
    _add("|------|------|------|------|--------|")
    for s, info in sorted(metrics.by_severity.items()):
        _add(
            f"| {s} | {info['total']} | {info['passed']} | {info['failed']} | "
            f"{info['pass_rate']:.1f}% |"
        )
    _add("")

    # ═══════════════════════════════════════════
    # Section 4: Tool Usage
    # ═══════════════════════════════════════════
    _add("## 四、工具调用统计")
    _add("")
    tool_counter = {}
    for r in metrics.results:
        pass
    # Detailed tool usage would require per-result tool data
    _add("（每个场景的工具调用详情见下）")
    _add("")

    # ═══════════════════════════════════════════
    # Section 5: Failure Analysis
    # ═══════════════════════════════════════════
    if metrics.failed > 0:
        _add("## 五、失败场景分析")
        _add("")
        _add(f"共 {metrics.failed} 个场景失败：")
        _add("")
        for failed_id in metrics.failed_scenarios:
            _add(f"- ✗ {failed_id}")
        _add("")

        if metrics.failure_reasons:
            _add("### 失败原因分布")
            _add("")
            _add("| 原因 | 次数 |")
            _add("|------|------|")
            for reason, count in metrics.failure_reasons.most_common():
                _add(f"| {reason} | {count} |")
            _add("")

    # ═══════════════════════════════════════════
    # Section 6: Detailed Results
    # ═══════════════════════════════════════════
    _add("## 六、场景详情")
    _add("")
    _add("| ID | 类型 | 难度 | 状态 | 步骤 | 工具调用 | Token | 耗时 |")
    _add("|----|------|------|------|------|----------|-------|------|")
    for r in metrics.results:
        status = "✅" if r.passed else "❌"
        _add(
            f"| {r.scenario_id} | {r.scenario_type} | {r.severity} | {status} | "
            f"{r.steps_count} | {r.tool_calls_count} | {r.total_tokens} | {r.duration_ms}ms |"
        )
    _add("")

    # ═══════════════════════════════════════════
    # Footer
    # ═══════════════════════════════════════════
    _add("---")
    _add("")
    _add(f"*报告由 QualiGuard Eval 自动生成 | {datetime.now().strftime('%Y-%m-%d %H:%M')}*")
    _add("")

    return "\n".join(lines)
