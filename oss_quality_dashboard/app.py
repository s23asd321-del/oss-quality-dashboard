"""Application entry point."""

from __future__ import annotations

import argparse
from pathlib import Path

import uvicorn

from .api import create_app
from .settings import DEFAULT_HOST, DEFAULT_PORT

app = create_app()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run the local OSS quality dashboard.")
    parser.add_argument("--host", default=DEFAULT_HOST, help="Bind host. Defaults to 127.0.0.1.")
    parser.add_argument("--port", default=DEFAULT_PORT, type=int, help="Bind port. Defaults to 8000.")
    parser.add_argument("--db-path", default=None, help="SQLite database path. Defaults to data/oss_quality_dashboard.sqlite.")
    args = parser.parse_args(argv)

    application = create_app(Path(args.db_path) if args.db_path else None)
    uvicorn.run(application, host=args.host, port=args.port)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

