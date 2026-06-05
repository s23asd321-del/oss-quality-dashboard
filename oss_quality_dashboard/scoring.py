"""Heuristic scoring for repository quality findings."""

from __future__ import annotations

from collections.abc import Iterable

ERROR_PENALTY = 10
WARNING_PENALTY = 4


def grade_for_score(score: int) -> str:
    if score >= 90:
        return "strong"
    if score >= 70:
        return "good"
    if score >= 50:
        return "needs work"
    return "risky"


def calculate_score(findings: Iterable[dict]) -> dict[str, int | str]:
    score = 100
    for finding in findings:
        severity = finding.get("severity")
        if severity == "error":
            score -= ERROR_PENALTY
        elif severity == "warning":
            score -= WARNING_PENALTY
    score = max(0, score)
    return {"score": score, "grade": grade_for_score(score)}

