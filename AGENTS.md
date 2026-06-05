# AGENTS.md

This project is a local-first OSS quality dashboard.

## Required Boundaries

- Default behavior must not access the network.
- Default service binding must remain `127.0.0.1`.
- Do not upload user files.
- Do not collect telemetry.
- Do not execute scripts from scanned repositories.
- Do not install dependencies from scanned repositories.
- Do not automatically modify scanned repositories.
- Do not delete or move user files.
- Do not output sensitive file contents.
- Do not follow symlinks inside scanned repositories to read content outside the explicitly selected tree.
- Do not add real tokens, passwords, cookies, API keys, credentials, or proxy subscription links.
- Do not add illegal, attack, evasion, cracking, piracy, abuse, or regulatory bypass content.

## Maintenance Rules

- New rules must include tests.
- API changes must update `docs/api.md`.
- Database schema changes must update `docs/database.md`.
- Scoring changes must update `docs/scoring-model.md`.
- CLI or UI behavior changes must update `README.md`.
- Security, privacy, and legal wording must stay conservative.
- Avoid unnecessary dependencies.

## First-Version Non-Goals

- Do not implement GitHub API integration.
- Do not implement AI suggestions.
- Do not implement remote scanning.
- Do not implement user accounts.
- Do not implement multi-tenant behavior.
- Do not implement cloud sync.
