"""Command-line interface for one-off local scans."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from .reports import generate_cli_payload, generate_markdown_report
from .scanner import scan_project
from .scoring import calculate_score


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="oss-quality", description="Local OSS quality dashboard utilities.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    scan_parser = subparsers.add_parser("scan", help="Scan a local repository path.")
    scan_parser.add_argument("path", help="Local repository directory to scan.")
    scan_parser.add_argument("--format", choices=["text", "markdown", "json"], default="text")
    scan_parser.add_argument("--output", help="Optional output file path.")

    args = parser.parse_args(argv)
    if args.command == "scan":
        return _scan(args.path, args.format, args.output)
    return 1


def _scan(path: str, output_format: str, output: str | None) -> int:
    result = scan_project(path)
    findings = result["findings"]
    scored = calculate_score(findings)
    payload = generate_cli_payload(str(Path(path).expanduser().resolve()), findings)
    payload["summary"] = {**result["summary"], **payload["summary"]}
    payload["score"] = scored["score"]
    payload["grade"] = scored["grade"]

    if output_format == "json":
        rendered = json.dumps(payload, indent=2, ensure_ascii=False)
    elif output_format == "markdown":
        scan = {
            "started_at": None,
            "finished_at": None,
            "score": payload["score"],
            "summary_json": payload["summary"],
        }
        rendered = generate_markdown_report({"name": Path(path).name, "path": str(Path(path).resolve())}, scan, findings)
    else:
        lines = [
            f"Project: {payload['project']['path']}",
            f"Score: {payload['score']} ({payload['grade']})",
            f"Findings: {payload['summary']['total_findings']}",
        ]
        for finding in findings:
            lines.append(f"- {finding['severity']}: {finding['rule_id']} {finding.get('path', '')}")
        rendered = "\n".join(lines)

    if output:
        Path(output).write_text(rendered, encoding="utf-8")
    else:
        sys.stdout.write(rendered)
        sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
