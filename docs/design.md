# Design

## Architecture

The first version is intentionally small:

- Static dashboard served by FastAPI.
- FastAPI API for projects, scans, reports, and summary.
- SQLite database accessed with standard-library `sqlite3`.
- Read-only scanner with built-in rules.
- Scoring module with a simple heuristic model.
- Report module for Markdown output.
- CLI for one-off local scans.

## Data Flow

1. User adds a local project path through the UI or API.
2. API validates that the path exists and is a directory.
3. API stores the project record in SQLite.
4. User triggers a scan.
5. Scanner reads only the specified directory, skipping ignored folders.
6. Scanner returns findings and summary data.
7. Scoring calculates score and grade.
8. API stores scan and findings.
9. UI renders score, findings, history, and report link.

## API Layer

The API is synchronous in the MVP. A scan runs during `POST /api/projects/{project_id}/scan` and returns the finished scan plus findings. This keeps the first version simple and avoids queues, Redis, Celery, and background worker complexity.

## DB Layer

`db.py` owns SQLite access. It avoids global long-lived connections and accepts a database path so tests can use temporary databases.

## Scanner

The scanner is read-only. It skips `.git`, dependency folders, virtual environments, caches, build output, and symlink targets. It does not execute code, install dependencies, follow symlinks to read outside the selected tree, or read risky file contents.

## Rules

Rules live in `rules.py` as structured metadata. Scanner behavior creates findings from those rules. New rules should have tests and conservative recommendations.

## Scoring

Scoring starts at 100. Errors subtract 10. Warnings subtract 4. Info findings do not subtract points. The score is never below 0.

## Reports

Reports are Markdown and include project, path, scan time, score, summary, findings by severity, recommendations, limitations, and safety/privacy notes. Local paths and sensitive-looking assignments are redacted on a best-effort basis.

## Static Frontend

The frontend is static HTML, CSS, and JavaScript. It does not use React, Vite, npm, CDNs, external fonts, or external APIs.

## Future Adapter Plan

Later versions may add adapters for existing local CLI tools such as `repo-readiness-kit`, `config-schema-guard`, `cli-golden-harness`, `markdown-link-auditor`, `structured-config-diff`, or `fixture-forge-lite`. The MVP does not depend on or call those projects.
