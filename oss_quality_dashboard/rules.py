"""Built-in local repository quality rules."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Rule:
    rule_id: str
    severity: str
    title: str
    message: str
    recommendation: str


RULES: dict[str, Rule] = {
    "R001_README_MISSING": Rule(
        "R001_README_MISSING",
        "error",
        "README.md is missing",
        "The repository does not contain a README.md file at the project root.",
        "Add a README.md that explains installation, usage, testing, license, security, privacy, and disclaimer notes.",
    ),
    "R002_LICENSE_MISSING": Rule(
        "R002_LICENSE_MISSING",
        "error",
        "License file is missing",
        "The repository does not contain LICENSE or LICENSE.md at the project root.",
        "Add a license file so users can understand the terms under which the project is shared.",
    ),
    "R003_GITIGNORE_MISSING": Rule(
        "R003_GITIGNORE_MISSING",
        "warning",
        ".gitignore is missing",
        "The repository does not contain a .gitignore file at the project root.",
        "Add a .gitignore that excludes local caches, virtual environments, logs, databases, and build output.",
    ),
    "R004_TESTS_MISSING": Rule(
        "R004_TESTS_MISSING",
        "warning",
        "Tests directory is missing",
        "The repository does not contain a tests/ directory.",
        "Add focused tests that cover the main behavior and document how to run them.",
    ),
    "R005_DOCS_MISSING": Rule(
        "R005_DOCS_MISSING",
        "warning",
        "Docs directory is missing",
        "The repository does not contain a docs/ directory.",
        "Add docs/ for design notes, API references, or usage details that do not fit in the README.",
    ),
    "R006_EXAMPLES_MISSING": Rule(
        "R006_EXAMPLES_MISSING",
        "info",
        "Examples directory is missing",
        "The repository does not contain an examples/ directory.",
        "Consider adding examples/ with safe demo inputs or common workflows.",
    ),
    "R007_SECURITY_MISSING": Rule(
        "R007_SECURITY_MISSING",
        "warning",
        "SECURITY.md is missing",
        "The repository does not contain SECURITY.md.",
        "Add SECURITY.md with conservative reporting guidance and project security boundaries.",
    ),
    "R008_PRIVACY_MISSING": Rule(
        "R008_PRIVACY_MISSING",
        "warning",
        "PRIVACY.md is missing",
        "The repository does not contain PRIVACY.md.",
        "Add PRIVACY.md that explains data handling, local storage, and sharing cautions.",
    ),
    "R009_DISCLAIMER_MISSING": Rule(
        "R009_DISCLAIMER_MISSING",
        "warning",
        "DISCLAIMER.md is missing",
        "The repository does not contain DISCLAIMER.md.",
        "Add DISCLAIMER.md to clarify non-goals and limits such as security, legal, compliance, and valuation claims.",
    ),
    "R010_CONTRIBUTING_MISSING": Rule(
        "R010_CONTRIBUTING_MISSING",
        "info",
        "CONTRIBUTING.md is missing",
        "The repository does not contain CONTRIBUTING.md.",
        "Consider adding contribution guidance for issues, pull requests, tests, docs, and rule changes.",
    ),
    "R011_CHANGELOG_MISSING": Rule(
        "R011_CHANGELOG_MISSING",
        "info",
        "CHANGELOG.md is missing",
        "The repository does not contain CHANGELOG.md.",
        "Consider adding a changelog so users can understand version changes.",
    ),
    "R012_CI_MISSING": Rule(
        "R012_CI_MISSING",
        "warning",
        "GitHub Actions workflow is missing",
        "The repository does not contain at least one .yml or .yaml file under .github/workflows.",
        "Add a minimal CI workflow that installs the project and runs the test suite.",
    ),
    "R013_RISKY_FILE_NAME": Rule(
        "R013_RISKY_FILE_NAME",
        "error",
        "Risky file name found",
        "A file name commonly associated with local secrets, logs, or databases was found.",
        "Review whether this file should be public. Do not publish reports that reveal sensitive paths or internal names.",
    ),
    "R014_README_INSTALL_SECTION_MISSING": Rule(
        "R014_README_INSTALL_SECTION_MISSING",
        "warning",
        "README installation section is missing",
        "README.md does not mention installation or setup.",
        "Add a short install or setup section with local development steps.",
    ),
    "R015_README_USAGE_SECTION_MISSING": Rule(
        "R015_README_USAGE_SECTION_MISSING",
        "warning",
        "README usage section is missing",
        "README.md does not mention usage.",
        "Add a usage section with at least one basic example.",
    ),
    "R016_README_TEST_SECTION_MISSING": Rule(
        "R016_README_TEST_SECTION_MISSING",
        "warning",
        "README testing section is missing",
        "README.md does not mention tests or testing.",
        "Add a test section that explains how to run the test suite.",
    ),
    "R017_README_LICENSE_SECTION_MISSING": Rule(
        "R017_README_LICENSE_SECTION_MISSING",
        "warning",
        "README license section is missing",
        "README.md does not mention the license.",
        "Add a license section that points to the repository license file.",
    ),
    "R018_LOCAL_ABSOLUTE_PATH_IN_README": Rule(
        "R018_LOCAL_ABSOLUTE_PATH_IN_README",
        "warning",
        "README contains a local absolute path",
        "README.md appears to contain a local absolute path such as a home directory or file:// URL.",
        "Replace local absolute paths with relative paths or redact them before sharing reports publicly.",
    ),
    "R019_PROJECT_METADATA_MISSING": Rule(
        "R019_PROJECT_METADATA_MISSING",
        "warning",
        "Project metadata file is missing",
        "The repository does not contain common project metadata such as pyproject.toml, package.json, Cargo.toml, or go.mod.",
        "Add the metadata file appropriate for the project's language and packaging model.",
    ),
    "R020_AGENTS_MISSING": Rule(
        "R020_AGENTS_MISSING",
        "info",
        "AGENTS.md is missing",
        "The repository does not contain AGENTS.md.",
        "Consider adding AGENTS.md with boundaries for AI coding agents and maintainers.",
    ),
    "R021_README_SECURITY_SECTION_MISSING": Rule(
        "R021_README_SECURITY_SECTION_MISSING",
        "warning",
        "README security section is missing",
        "README.md does not mention security.",
        "Add a conservative security section that points to SECURITY.md and avoids overclaiming.",
    ),
    "R022_README_PRIVACY_SECTION_MISSING": Rule(
        "R022_README_PRIVACY_SECTION_MISSING",
        "warning",
        "README privacy section is missing",
        "README.md does not mention privacy.",
        "Add a privacy section that explains local data handling and report sharing cautions.",
    ),
    "R023_README_DISCLAIMER_SECTION_MISSING": Rule(
        "R023_README_DISCLAIMER_SECTION_MISSING",
        "warning",
        "README disclaimer section is missing",
        "README.md does not mention disclaimers or limitations.",
        "Add a disclaimer section that clarifies what the project does not guarantee.",
    ),
    "R024_CODE_OF_CONDUCT_MISSING": Rule(
        "R024_CODE_OF_CONDUCT_MISSING",
        "info",
        "CODE_OF_CONDUCT.md is missing",
        "The repository does not contain CODE_OF_CONDUCT.md.",
        "Consider adding a code of conduct if community contribution is expected.",
    ),
    "R025_ROADMAP_MISSING": Rule(
        "R025_ROADMAP_MISSING",
        "info",
        "ROADMAP.md is missing",
        "The repository does not contain ROADMAP.md.",
        "Consider adding ROADMAP.md to explain planned work and non-goals.",
    ),
    "R026_TODO_MISSING": Rule(
        "R026_TODO_MISSING",
        "info",
        "TODO.md is missing",
        "The repository does not contain TODO.md.",
        "Consider tracking short-term cleanup or follow-up work in TODO.md.",
    ),
    "R027_SYMLINK_SKIPPED": Rule(
        "R027_SYMLINK_SKIPPED",
        "info",
        "Symlink skipped",
        "A symlink was found and skipped so the scanner does not read outside the explicit repository tree.",
        "Review whether the symlink is intentional. Prefer regular files for public repository quality signals.",
    ),
}


def get_rule(rule_id: str) -> Rule:
    return RULES[rule_id]


def make_finding(rule_id: str, path: str = "") -> dict[str, str]:
    rule = get_rule(rule_id)
    return {
        "rule_id": rule.rule_id,
        "severity": rule.severity,
        "title": rule.title,
        "message": rule.message,
        "path": path,
        "recommendation": rule.recommendation,
    }
