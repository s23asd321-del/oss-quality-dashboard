# Contributing

Thanks for considering a contribution.

## Principles

- Keep the project local-first.
- Preserve the default `127.0.0.1` binding.
- Avoid unnecessary dependencies.
- Do not add code that uploads files, collects telemetry, or executes scanned repository scripts.
- Keep security, privacy, and legal wording conservative.

## Pull Requests

- Add or update tests for behavior changes.
- Update docs when API, database, scoring, CLI, UI, or rule behavior changes.
- Do not include real secrets, private paths, raw private logs, personal email addresses, or internal URLs.

## Rule Changes

New rules should include:

- A clear rule ID
- Severity
- Purpose
- False-positive notes
- Test coverage
- A conservative recommendation

