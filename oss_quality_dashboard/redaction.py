"""Best-effort redaction helpers for reports and API output."""

from __future__ import annotations

import re

LOCAL_PATH_PATTERNS = [
    re.compile(r"/Users/([^/\s)]+)"),
    re.compile(r"/home/([^/\s)]+)"),
    re.compile(r"C:\\Users\\([^\\\s)]+)", re.IGNORECASE),
]

FILE_URL_PATTERN = re.compile(r"file://[^\s)]+", re.IGNORECASE)
SENSITIVE_ASSIGNMENT_PATTERN = re.compile(
    r"(?i)\b(token|password|passwd|secret|cookie|api[_-]?key|credential)\b\s*([:=])\s*([^\s]+)"
)


def redact_local_paths(text: str) -> str:
    """Redact common local home-directory prefixes without claiming completeness."""

    redacted = FILE_URL_PATTERN.sub("file://<redacted-local-path>", text)
    for pattern in LOCAL_PATH_PATTERNS:
        redacted = pattern.sub(lambda match: match.group(0).replace(match.group(1), "<redacted>"), redacted)
    return redacted


def redact_sensitive_terms(text: str) -> str:
    """Redact obvious key/value strings that use sensitive-looking names."""

    return SENSITIVE_ASSIGNMENT_PATTERN.sub(lambda match: f"{match.group(1)}{match.group(2)}<redacted>", text)


def redact_text(text: str) -> str:
    """Apply all conservative redaction helpers."""

    return redact_sensitive_terms(redact_local_paths(text))

