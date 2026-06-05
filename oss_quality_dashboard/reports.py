"""Markdown and JSON-compatible report generation."""

from __future__ import annotations

from collections import defaultdict
from datetime import UTC, datetime
from typing import Any

from .redaction import redact_text
from .scoring import calculate_score


def build_summary(findings: list[dict], score: int | None = None, grade: str | None = None) -> dict[str, Any]:
    scored = calculate_score(findings) if score is None or grade is None else {"score": score, "grade": grade}
    severity_counts = {"error": 0, "warning": 0, "info": 0}
    for finding in findings:
        severity = finding.get("severity")
        if severity in severity_counts:
            severity_counts[severity] += 1
    return {
        "score": scored["score"],
        "grade": scored["grade"],
        "total_findings": len(findings),
        "severity_counts": severity_counts,
    }


def generate_markdown_report(project: dict, scan: dict, findings: list[dict]) -> str:
    summary = scan.get("summary_json") or build_summary(findings, scan.get("score"))
    grouped: dict[str, list[dict]] = defaultdict(list)
    for finding in findings:
        grouped[finding.get("severity", "info")].append(finding)

    lines = [
        f"# OSS Quality Report: {project.get('name', 'Unknown project')}",
        "",
        "## Project",
        "",
        f"- Project: {redact_text(str(project.get('name', 'Unknown project')))}",
        f"- Path: {redact_text(str(project.get('path', '')))}",
        f"- Scan time: {scan.get('finished_at') or scan.get('started_at') or _now()}",
        f"- Score: {scan.get('score', summary.get('score'))} ({summary.get('grade', 'unknown')})",
        "",
        "## Summary",
        "",
        f"- Total findings: {summary.get('total_findings', len(findings))}",
        f"- Errors: {summary.get('severity_counts', {}).get('error', 0)}",
        f"- Warnings: {summary.get('severity_counts', {}).get('warning', 0)}",
        f"- Info: {summary.get('severity_counts', {}).get('info', 0)}",
        "",
    ]
    for severity, heading in (("error", "Errors"), ("warning", "Warnings"), ("info", "Info")):
        lines.extend([f"## {heading}", ""])
        items = grouped.get(severity, [])
        if not items:
            lines.extend(["No findings.", ""])
            continue
        for finding in items:
            lines.extend(
                [
                    f"### {finding.get('rule_id')} - {finding.get('title')}",
                    "",
                    f"- Path: {redact_text(str(finding.get('path', '')))}",
                    f"- Message: {redact_text(str(finding.get('message', '')))}",
                    f"- Recommendation: {redact_text(str(finding.get('recommendation', '')))}",
                    "",
                ]
            )

    recommendations = sorted({finding.get("recommendation", "") for finding in findings if finding.get("recommendation")})
    lines.extend(["## Recommendations", ""])
    if recommendations:
        for recommendation in recommendations:
            lines.append(f"- {redact_text(str(recommendation))}")
    else:
        lines.append("- No recommendations from the current rule set.")
    lines.extend(
        [
            "",
            "## Limitations",
            "",
            "- This score is a heuristic reference only.",
            "- It does not represent security, legal, privacy, compliance, or project value assurance.",
            "- This tool is not a secret scanner, vulnerability scanner, legal review, or privacy compliance certification.",
            "",
            "## Safety and privacy notes",
            "",
            "- The scanner is designed for explicitly added local directories.",
            "- It does not upload repository contents or collect telemetry.",
            "- Reports may still include project names and relative file paths; review reports before publishing.",
            "- Risky file name checks report paths and rule names only, not file contents.",
            "",
        ]
    )
    return "\n".join(lines)


def generate_cli_payload(project_path: str, findings: list[dict]) -> dict[str, Any]:
    summary = build_summary(findings)
    return {
        "project": {"path": redact_text(project_path)},
        "score": summary["score"],
        "grade": summary["grade"],
        "summary": summary,
        "findings": findings,
    }


def _now() -> str:
    return datetime.now(UTC).isoformat()

