from oss_quality_dashboard.scoring import calculate_score, grade_for_score


def test_scoring_with_no_findings_returns_100():
    assert calculate_score([]) == {"score": 100, "grade": "strong"}


def test_scoring_with_errors_and_warnings_deducts_points():
    findings = [{"severity": "error"}, {"severity": "warning"}, {"severity": "info"}]
    assert calculate_score(findings) == {"score": 86, "grade": "good"}


def test_grade_boundaries():
    assert grade_for_score(90) == "strong"
    assert grade_for_score(70) == "good"
    assert grade_for_score(50) == "needs work"
    assert grade_for_score(49) == "risky"

