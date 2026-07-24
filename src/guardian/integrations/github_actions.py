from __future__ import annotations
from guardian.core.models import Issue, Severity


def format_annotation(issue: Issue) -> str:
    level = {"error": "error", "warning": "warning", "info": "notice"}[issue.severity.value]
    return f":{level} file={issue.file_path},line={issue.line}," + f"title={issue.rule_id}::{issue.message}"


def generate_summary(issues: list[Issue]) -> str:
    lines = ["## QualiGuard 代码质量检查报告"]
    lines.append("")
    if not issues:
        lines.append(":white_check_mark: 未发现问题，代码质量良好！")
        lines.append("")
        return "\n".join(lines)
    errors = sum(1 for i in issues if i.severity == Severity.ERROR)
    warnings = sum(1 for i in issues if i.severity == Severity.WARNING)
    infos = sum(1 for i in issues if i.severity == Severity.INFO)
    lines.append("| 类别 | 数量 |")
    lines.append("|---|---|")
    lines.append(f":red_circle: 严重错误 Errors | {errors} |")
    lines.append(f":yellow_circle: 警告 Warnings | {warnings} |")
    lines.append(f":blue_circle: 提示 Info | {infos} |")
    lines.append(f"| **合计** | **{len(issues)}** |")
    lines.append("")
    for i, issue in enumerate(issues[:20], 1):
        em = ":red_circle:" if issue.severity == Severity.ERROR else ":yellow_circle:" if issue.severity == Severity.WARNING else ":blue_circle:"
        lines.append(f"{em} **{issue.rule_id}**: {issue.message}")
        lines.append(f"   {issue.file_path}:{issue.line}")
        lines.append("")
    if len(issues) > 20:
        lines.append(f"... 还有 {len(issues) - 20} 个问题，查看 SARIF 报告获取全量。")
        lines.append("")
    return "\n".join(lines)
