from pathlib import Path

from oss_quality_dashboard.reports import generate_markdown_report
from oss_quality_dashboard.scanner import scan_project


def _ids(result):
    return {finding["rule_id"] for finding in result["findings"]}


def _write_minimal_good_repo(root: Path):
    (root / "README.md").write_text(
        """
# Demo

## Installation
install locally.

## Usage
use locally.

## Testing
run tests.

## License
MIT.

## Security
local fixture.

## Privacy
no telemetry.

## Disclaimer
heuristic only.
""",
        encoding="utf-8",
    )
    (root / "LICENSE").write_text("MIT", encoding="utf-8")
    (root / ".gitignore").write_text(".env\n", encoding="utf-8")
    (root / "pyproject.toml").write_text("[project]\nname='demo'\n", encoding="utf-8")
    for directory in ["tests", "docs", "examples", ".github/workflows"]:
        (root / directory).mkdir(parents=True, exist_ok=True)
    (root / ".github/workflows/ci.yml").write_text("name: CI\n", encoding="utf-8")
    for filename in [
        "SECURITY.md",
        "PRIVACY.md",
        "DISCLAIMER.md",
        "CONTRIBUTING.md",
        "CHANGELOG.md",
        "AGENTS.md",
        "CODE_OF_CONDUCT.md",
        "ROADMAP.md",
        "TODO.md",
    ]:
        (root / filename).write_text("demo", encoding="utf-8")


def test_readme_missing_rule(tmp_path):
    result = scan_project(tmp_path)
    assert "R001_README_MISSING" in _ids(result)


def test_license_missing_rule(tmp_path):
    (tmp_path / "README.md").write_text("install usage test license security privacy disclaimer", encoding="utf-8")
    result = scan_project(tmp_path)
    assert "R002_LICENSE_MISSING" in _ids(result)


def test_ci_missing_rule(tmp_path):
    _write_minimal_good_repo(tmp_path)
    (tmp_path / ".github/workflows/ci.yml").unlink()
    result = scan_project(tmp_path)
    assert "R012_CI_MISSING" in _ids(result)


def test_risky_file_name_rule(tmp_path):
    _write_minimal_good_repo(tmp_path)
    (tmp_path / ".env").write_text("DEMO_ONLY_NOT_A_REAL_SECRET", encoding="utf-8")
    result = scan_project(tmp_path)
    assert "R013_RISKY_FILE_NAME" in _ids(result)


def test_readme_section_rules(tmp_path):
    _write_minimal_good_repo(tmp_path)
    (tmp_path / "README.md").write_text("# Demo\n\nUsage only.\n", encoding="utf-8")
    result = scan_project(tmp_path)
    ids = _ids(result)
    assert "R014_README_INSTALL_SECTION_MISSING" in ids
    assert "R016_README_TEST_SECTION_MISSING" in ids
    assert "R017_README_LICENSE_SECTION_MISSING" in ids


def test_local_absolute_path_rule(tmp_path):
    _write_minimal_good_repo(tmp_path)
    (tmp_path / "README.md").write_text(
        "install usage test license security privacy disclaimer /Users/demo-user/internal",
        encoding="utf-8",
    )
    result = scan_project(tmp_path)
    assert "R018_LOCAL_ABSOLUTE_PATH_IN_README" in _ids(result)


def test_scanner_ignores_git_node_modules_and_venv(tmp_path):
    _write_minimal_good_repo(tmp_path)
    for directory in [".git", "node_modules", ".venv"]:
        ignored = tmp_path / directory
        ignored.mkdir()
        (ignored / ".env").write_text("DEMO_ONLY_NOT_A_REAL_SECRET", encoding="utf-8")

    result = scan_project(tmp_path)
    paths = {finding["path"] for finding in result["findings"]}

    assert ".git/.env" not in paths
    assert "node_modules/.env" not in paths
    assert ".venv/.env" not in paths


def test_scanner_does_not_read_risky_file_contents(tmp_path):
    _write_minimal_good_repo(tmp_path)
    marker = "DEMO_MARKER_SHOULD_NOT_APPEAR_IN_REPORT"
    (tmp_path / "local.db").write_text(marker, encoding="utf-8")
    result = scan_project(tmp_path)
    report = generate_markdown_report(
        {"name": "repo", "path": str(tmp_path)},
        {"score": 90, "summary_json": {"grade": "strong", "severity_counts": {}}},
        result["findings"],
    )

    assert "R013_RISKY_FILE_NAME" in _ids(result)
    assert marker not in report


def test_scanner_skips_readme_symlink_contents(tmp_path):
    repo = tmp_path / "repo"
    outside = tmp_path / "outside"
    repo.mkdir()
    outside.mkdir()
    _write_minimal_good_repo(repo)
    marker = "DEMO_MARKER_SYMLINK_README_SHOULD_NOT_APPEAR"
    outside_readme = outside / "README.md"
    outside_readme.write_text(
        f"install usage test license security privacy disclaimer {marker}",
        encoding="utf-8",
    )
    (repo / "README.md").unlink()
    (repo / "README.md").symlink_to(outside_readme)

    result = scan_project(repo)
    report = generate_markdown_report(
        {"name": "repo", "path": str(repo)},
        {"score": 90, "summary_json": {"grade": "strong", "severity_counts": {}}},
        result["findings"],
    )

    assert "R027_SYMLINK_SKIPPED" in _ids(result)
    assert "R001_README_MISSING" in _ids(result)
    assert marker not in report
    assert result["summary"]["skipped_symlink_count"] == 1


def test_scanner_reports_risky_symlink_name_without_reading_contents(tmp_path):
    repo = tmp_path / "repo"
    outside = tmp_path / "outside"
    repo.mkdir()
    outside.mkdir()
    _write_minimal_good_repo(repo)
    marker = "DEMO_MARKER_RISKY_SYMLINK_SHOULD_NOT_APPEAR"
    outside_file = outside / "fixture.txt"
    outside_file.write_text(marker, encoding="utf-8")
    (repo / ".env").symlink_to(outside_file)

    result = scan_project(repo)
    report = generate_markdown_report(
        {"name": "repo", "path": str(repo)},
        {"score": 90, "summary_json": {"grade": "strong", "severity_counts": {}}},
        result["findings"],
    )

    ids = _ids(result)
    assert "R013_RISKY_FILE_NAME" in ids
    assert "R027_SYMLINK_SKIPPED" in ids
    assert marker not in report
