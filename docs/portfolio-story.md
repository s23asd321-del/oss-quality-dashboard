# Portfolio Story

`oss-quality-dashboard` demonstrates a complete but bounded engineering project.

## Capabilities Demonstrated

- API design with FastAPI endpoints and predictable request/response shapes.
- SQLite data modeling for projects, scans, and findings.
- Local Web UI with static HTML, CSS, and JavaScript.
- Rule engine design with structured metadata and scanner behavior.
- Report generation with Markdown output and conservative redaction.
- Test coverage across database, rules, scanner, scoring, reports, API, CLI, and static serving.
- Docker and Docker Compose support for local container runs.
- GitHub Actions CI for Python 3.11 and 3.12.
- Security and privacy boundaries that are explicit in code and documentation.
- Documentation across architecture, API, database, scoring, rules, and release workflow.
- Defensive scanner behavior such as skipped symlinks, ignored dependency/cache folders, and no risky file content output.

## Honest Limits

- The first version is not an enterprise product.
- It has no multi-user authentication.
- It does not implement cloud deployment.
- It does not perform real security scanning.
- It does not call the GitHub API.
- It does not guarantee a project is safe, compliant, valuable, or ready to publish.

## Relationship To Other Local Tools

Future versions may add adapters for existing local CLI tools, but the MVP is independent and runs without those projects.
