from oss_quality_dashboard.rules import RULES, make_finding


def test_rule_metadata_contains_required_rules():
    for rule_id in [
        "R001_README_MISSING",
        "R002_LICENSE_MISSING",
        "R012_CI_MISSING",
        "R013_RISKY_FILE_NAME",
        "R020_AGENTS_MISSING",
        "R027_SYMLINK_SKIPPED",
    ]:
        assert rule_id in RULES
        assert RULES[rule_id].severity in {"info", "warning", "error"}


def test_make_finding_uses_rule_metadata():
    finding = make_finding("R001_README_MISSING", "README.md")

    assert finding["severity"] == "error"
    assert finding["path"] == "README.md"
    assert "README" in finding["title"]
