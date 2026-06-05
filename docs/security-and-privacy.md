# Security And Privacy

## Local Running

The dashboard binds to `127.0.0.1` by default and is intended for local development. Do not expose it to the public internet without authentication and access controls.

## No Default Network Access

The scanner does not call external APIs. The static frontend calls only the local API served by the app.

## No Uploads Or Telemetry

The project does not upload repository contents and does not collect telemetry.

## Explicit Directories Only

The scanner runs only on project directories added by the user through the API, UI, or CLI.

## No Code Execution

The scanner does not execute scripts from scanned repositories and does not install scanned repository dependencies.

## Symlinks

The scanner does not follow symlinks to read file contents. Symlinks are reported as skipped so users can review them without the tool reading outside the explicitly selected tree.

## Risky File Contents

Risky file name checks report paths and rule IDs only. They do not read or print file contents.

## Reports

Reports may include project names and file paths. Public sharing should be done only after reviewing and redacting sensitive internal details.

## Non-Goals

This project is not a secret scanner, vulnerability scanner, security audit, legal review, privacy compliance certification, or public release guarantee.
