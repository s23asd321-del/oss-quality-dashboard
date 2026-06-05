"""Read-only local repository scanner."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
import re

from .redaction import redact_text
from .rules import make_finding
from .settings import IGNORED_DIR_NAMES, MAX_TEXT_FILE_BYTES

METADATA_FILES = {
    "pyproject.toml",
    "package.json",
    "Cargo.toml",
    "go.mod",
    "package.swift",
    "Gemfile",
    "pom.xml",
    "build.gradle",
    "composer.json",
}

RISKY_EXACT_NAMES = {".env", ".env.local", ".env.production"}
RISKY_SUFFIXES = (".pem", ".key", ".sqlite", ".db", ".log")
README_SECTION_RULES = {
    "R014_README_INSTALL_SECTION_MISSING": ("installation", "install", "安装"),
    "R015_README_USAGE_SECTION_MISSING": ("usage", "使用"),
    "R016_README_TEST_SECTION_MISSING": ("test", "testing", "测试"),
    "R017_README_LICENSE_SECTION_MISSING": ("license", "许可证"),
    "R021_README_SECURITY_SECTION_MISSING": ("security", "安全"),
    "R022_README_PRIVACY_SECTION_MISSING": ("privacy", "隐私"),
    "R023_README_DISCLAIMER_SECTION_MISSING": ("disclaimer", "免责声明"),
}
LOCAL_PATH_PATTERN = re.compile(r"(/Users/[^\s)]+|/home/[^\s)]+|C:\\Users\\[^\s)]+|file://[^\s)]+)", re.IGNORECASE)


def scan_project(project_path: str | Path, max_text_file_bytes: int = MAX_TEXT_FILE_BYTES) -> dict:
    """Scan a user-specified local project directory without executing code."""

    root = Path(project_path).expanduser().resolve()
    if not root.exists() or not root.is_dir():
        raise ValueError(f"Project path must be an existing directory: {project_path}")

    findings: list[dict] = []
    readme_path = root / "README.md"

    if not _is_real_file(readme_path):
        findings.append(make_finding("R001_README_MISSING", "README.md"))
    if not (_is_real_file(root / "LICENSE") or _is_real_file(root / "LICENSE.md")):
        findings.append(make_finding("R002_LICENSE_MISSING", "LICENSE"))
    if not _is_real_file(root / ".gitignore"):
        findings.append(make_finding("R003_GITIGNORE_MISSING", ".gitignore"))
    if not _is_real_dir(root / "tests"):
        findings.append(make_finding("R004_TESTS_MISSING", "tests/"))
    if not _is_real_dir(root / "docs"):
        findings.append(make_finding("R005_DOCS_MISSING", "docs/"))
    if not _is_real_dir(root / "examples"):
        findings.append(make_finding("R006_EXAMPLES_MISSING", "examples/"))
    if not _is_real_file(root / "SECURITY.md"):
        findings.append(make_finding("R007_SECURITY_MISSING", "SECURITY.md"))
    if not _is_real_file(root / "PRIVACY.md"):
        findings.append(make_finding("R008_PRIVACY_MISSING", "PRIVACY.md"))
    if not _is_real_file(root / "DISCLAIMER.md"):
        findings.append(make_finding("R009_DISCLAIMER_MISSING", "DISCLAIMER.md"))
    if not _is_real_file(root / "CONTRIBUTING.md"):
        findings.append(make_finding("R010_CONTRIBUTING_MISSING", "CONTRIBUTING.md"))
    if not _is_real_file(root / "CHANGELOG.md"):
        findings.append(make_finding("R011_CHANGELOG_MISSING", "CHANGELOG.md"))
    if not _has_ci_workflow(root):
        findings.append(make_finding("R012_CI_MISSING", ".github/workflows/"))
    if not _has_project_metadata(root):
        findings.append(make_finding("R019_PROJECT_METADATA_MISSING", "project metadata"))
    if not _is_real_file(root / "AGENTS.md"):
        findings.append(make_finding("R020_AGENTS_MISSING", "AGENTS.md"))
    if not _is_real_file(root / "CODE_OF_CONDUCT.md"):
        findings.append(make_finding("R024_CODE_OF_CONDUCT_MISSING", "CODE_OF_CONDUCT.md"))
    if not _is_real_file(root / "ROADMAP.md"):
        findings.append(make_finding("R025_ROADMAP_MISSING", "ROADMAP.md"))
    if not _is_real_file(root / "TODO.md"):
        findings.append(make_finding("R026_TODO_MISSING", "TODO.md"))

    if _is_real_file(readme_path):
        readme = _read_text_if_safe(readme_path, max_text_file_bytes)
        if readme is not None:
            lower_readme = readme.lower()
            for rule_id, keywords in README_SECTION_RULES.items():
                if not any(keyword.lower() in lower_readme for keyword in keywords):
                    findings.append(make_finding(rule_id, "README.md"))
            if LOCAL_PATH_PATTERN.search(readme):
                finding = make_finding("R018_LOCAL_ABSOLUTE_PATH_IN_README", "README.md")
                finding["message"] = redact_text(finding["message"])
                findings.append(finding)

    skipped_symlink_count = 0
    for path, is_symlink in _iter_file_candidates(root):
        if is_symlink:
            skipped_symlink_count += 1
            if _is_risky_file_name(path.name):
                findings.append(make_finding("R013_RISKY_FILE_NAME", _relative_path(root, path)))
            findings.append(make_finding("R027_SYMLINK_SKIPPED", _relative_path(root, path)))
            continue
        if _is_risky_file_name(path.name):
            findings.append(make_finding("R013_RISKY_FILE_NAME", _relative_path(root, path)))

    severity_counts = Counter(finding["severity"] for finding in findings)
    rule_counts = Counter(finding["rule_id"] for finding in findings)
    summary = {
        "project_path": redact_text(str(root)),
        "total_findings": len(findings),
        "severity_counts": dict(severity_counts),
        "rule_counts": dict(rule_counts),
        "ignored_directories": sorted(IGNORED_DIR_NAMES),
        "skipped_symlink_count": skipped_symlink_count,
    }
    return {"findings": findings, "summary": summary}


def _has_ci_workflow(root: Path) -> bool:
    workflows = root / ".github" / "workflows"
    if not _is_real_dir(workflows):
        return False
    return any(_is_real_file(path) and path.suffix.lower() in {".yml", ".yaml"} for path in workflows.iterdir())


def _has_project_metadata(root: Path) -> bool:
    return any(_is_real_file(root / filename) for filename in METADATA_FILES)


def _iter_file_candidates(root: Path):
    for path in root.rglob("*"):
        if any(part in IGNORED_DIR_NAMES for part in path.relative_to(root).parts[:-1]):
            continue
        if path.is_symlink():
            yield path, True
        elif path.is_file():
            yield path, False


def _is_risky_file_name(name: str) -> bool:
    lower_name = name.lower()
    return lower_name in RISKY_EXACT_NAMES or lower_name.endswith(RISKY_SUFFIXES)


def _read_text_if_safe(path: Path, max_bytes: int) -> str | None:
    if path.is_symlink():
        return None
    try:
        if path.stat().st_size > max_bytes:
            return None
        data = path.read_bytes()
    except OSError:
        return None
    if b"\x00" in data:
        return None
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return None


def _relative_path(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def _is_real_file(path: Path) -> bool:
    return path.exists() and not path.is_symlink() and path.is_file()


def _is_real_dir(path: Path) -> bool:
    return path.exists() and not path.is_symlink() and path.is_dir()
