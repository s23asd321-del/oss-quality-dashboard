from oss_quality_dashboard.reports import generate_markdown_report
from oss_quality_dashboard.rules import make_finding


def test_markdown_report_contains_score_and_summary():
    finding = make_finding("R001_README_MISSING", "README.md")
    report = generate_markdown_report(
        {"name": "repo", "path": "/Users/demo-user/repo"},
        {"score": 90, "summary_json": {"grade": "strong", "total_findings": 1, "severity_counts": {"error": 1}}},
        [finding],
    )

    assert "Score: 90" in report
    assert "## Summary" in report
    assert "/Users/<redacted>/repo" in report


def test_markdown_report_does_not_include_risky_file_content():
    finding = make_finding("R013_RISKY_FILE_NAME", ".env")
    report = generate_markdown_report(
        {"name": "repo", "path": "/repo"},
        {"score": 90, "summary_json": {"grade": "strong", "total_findings": 1, "severity_counts": {"error": 1}}},
        [finding],
    )

    assert "FAKE_VALUE_FOR_TESTING_ONLY" not in report
    assert ".env" in report

