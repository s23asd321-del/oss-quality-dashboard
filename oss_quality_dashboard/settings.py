"""Application settings."""

from __future__ import annotations

import os
from pathlib import Path

APP_NAME = "oss-quality-dashboard"
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8000
DEFAULT_DATABASE_PATH = Path(os.environ.get("OSS_QUALITY_DB_PATH", "data/oss_quality_dashboard.sqlite"))
MAX_TEXT_FILE_BYTES = 512 * 1024

IGNORED_DIR_NAMES = {
    ".git",
    "node_modules",
    ".venv",
    "venv",
    "dist",
    "build",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
}

