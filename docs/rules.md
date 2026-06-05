# Rules

Rules are local, read-only checks. They do not call external services and do not execute scanned repository code.

| Rule | Severity | Purpose | False-positive notes | Suggested fix |
| --- | --- | --- | --- | --- |
| R001_README_MISSING | error | Check root README.md presence | Some internal repos may intentionally omit README | Add README.md |
| R002_LICENSE_MISSING | error | Check LICENSE or LICENSE.md presence | Private repos may not need public license text | Add an appropriate license file |
| R003_GITIGNORE_MISSING | warning | Check .gitignore presence | Some generated repos may not need one | Add .gitignore |
| R004_TESTS_MISSING | warning | Check tests/ presence | Tests may live elsewhere | Add tests/ or document layout |
| R005_DOCS_MISSING | warning | Check docs/ presence | Small repos may keep all docs in README | Add docs/ for design or API notes |
| R006_EXAMPLES_MISSING | info | Check examples/ presence | Libraries may not need examples | Add examples/ if useful |
| R007_SECURITY_MISSING | warning | Check SECURITY.md presence | Small projects may only use README security text | Add SECURITY.md |
| R008_PRIVACY_MISSING | warning | Check PRIVACY.md presence | Some tools may not process data | Add PRIVACY.md with conservative notes |
| R009_DISCLAIMER_MISSING | warning | Check DISCLAIMER.md presence | Some repos may put limitations in README | Add DISCLAIMER.md |
| R010_CONTRIBUTING_MISSING | info | Check CONTRIBUTING.md presence | Single-maintainer repos may not accept contributions | Add contribution guidance |
| R011_CHANGELOG_MISSING | info | Check CHANGELOG.md presence | Early repos may not have releases yet | Add Keep a Changelog style file |
| R012_CI_MISSING | warning | Check .github/workflows with yml/yaml | CI may run outside GitHub | Add a minimal workflow or document CI |
| R013_RISKY_FILE_NAME | error | Flag risky file names such as .env, .pem, .db, .log | Demo fixtures may be intentionally included | Review before publishing; do not expose sensitive files |
| R014_README_INSTALL_SECTION_MISSING | warning | Check README install/setup topic | Install may be trivial | Add install or setup section |
| R015_README_USAGE_SECTION_MISSING | warning | Check README usage topic | Some repos are not user-facing | Add usage section |
| R016_README_TEST_SECTION_MISSING | warning | Check README test topic | Tests may be documented elsewhere | Add test command |
| R017_README_LICENSE_SECTION_MISSING | warning | Check README license topic | License may be clear from LICENSE file | Add license section |
| R018_LOCAL_ABSOLUTE_PATH_IN_README | warning | Flag obvious local absolute paths in README | Intentional local examples may trigger it | Use relative paths or redact before sharing |
| R019_PROJECT_METADATA_MISSING | warning | Check common metadata files | Some repos may be docs-only | Add language-appropriate metadata |
| R020_AGENTS_MISSING | info | Check AGENTS.md presence | Not every repo uses AI agent guidance | Add AGENTS.md if helpful |
| R021_README_SECURITY_SECTION_MISSING | warning | Check README security topic | SECURITY.md may be enough for some projects | Add brief README security pointer |
| R022_README_PRIVACY_SECTION_MISSING | warning | Check README privacy topic | Privacy may be covered elsewhere | Add privacy section |
| R023_README_DISCLAIMER_SECTION_MISSING | warning | Check README disclaimer topic | Limitations may be in docs | Add disclaimer or limitations section |
| R024_CODE_OF_CONDUCT_MISSING | info | Check CODE_OF_CONDUCT.md presence | Some repos do not accept outside contributors | Add code of conduct if community-facing |
| R025_ROADMAP_MISSING | info | Check ROADMAP.md presence | Roadmap may be tracked elsewhere | Add roadmap or non-goals |
| R026_TODO_MISSING | info | Check TODO.md presence | Tasks may live in issues | Add TODO.md if useful |
| R027_SYMLINK_SKIPPED | info | Report skipped symlinks | Some repos intentionally use symlinks | Review symlinks and prefer regular files for public quality signals |

## Sensitive Data

`R013_RISKY_FILE_NAME` reports file names and paths only. It does not read or output risky file contents.

## Symlinks

The scanner reports symlinks with `R027_SYMLINK_SKIPPED` and does not follow them to read file contents. This protects the local-first boundary when a repository contains links to files outside the explicitly selected tree.
