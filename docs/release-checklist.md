# Release Checklist

- `python -m pytest` passes.
- `examples/sample-good-repo` scan completes and receives a high score.
- `examples/sample-risky-repo` triggers expected findings.
- Docker build succeeds if the environment supports Docker.
- README is updated.
- Docs are updated.
- CHANGELOG is updated.
- Examples contain no real sensitive information.
- GitHub Actions CI is present and expected to run.
- Repository does not include `.venv`, `__pycache__`, `.pytest_cache`, `dist`, `build`, or `*.egg-info`.
- Public reports are checked for sensitive local paths or internal project names.
- No automatic Git init, commit, push, upload, or deploy behavior is present.

Before a public release, consider enabling Dependabot, secret scanning, push protection, and code scanning if the repository or account supports them.

