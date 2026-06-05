import json

from oss_quality_dashboard.cli import main


def test_cli_scan_returns_0_for_sample_good_repo(capsys):
    exit_code = main(["scan", "examples/sample-good-repo", "--format", "markdown"])
    output = capsys.readouterr().out

    assert exit_code == 0
    assert "# OSS Quality Report" in output
    assert "Score: 100" in output


def test_cli_scan_returns_expected_findings_for_sample_risky_repo(capsys):
    exit_code = main(["scan", "examples/sample-risky-repo", "--format", "json"])
    output = capsys.readouterr().out
    payload = json.loads(output)
    rule_ids = {finding["rule_id"] for finding in payload["findings"]}

    assert exit_code == 0
    assert "R013_RISKY_FILE_NAME" in rule_ids
    assert "R002_LICENSE_MISSING" in rule_ids

