"""SQLite persistence layer."""

from __future__ import annotations

from datetime import UTC, datetime
import json
from pathlib import Path
import sqlite3
from typing import Any

from .settings import DEFAULT_DATABASE_PATH


def get_connection(db_path: str | Path | None = None) -> sqlite3.Connection:
    path = Path(db_path or DEFAULT_DATABASE_PATH)
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def init_db(db_path: str | Path | None = None) -> None:
    with get_connection(db_path) as connection:
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                path TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS scans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER NOT NULL,
                started_at TEXT NOT NULL,
                finished_at TEXT,
                status TEXT NOT NULL,
                score INTEGER,
                summary_json TEXT NOT NULL DEFAULT '{}',
                FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS findings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                scan_id INTEGER NOT NULL,
                rule_id TEXT NOT NULL,
                severity TEXT NOT NULL,
                title TEXT NOT NULL,
                message TEXT NOT NULL,
                path TEXT NOT NULL,
                recommendation TEXT NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY (scan_id) REFERENCES scans(id) ON DELETE CASCADE
            );

            CREATE UNIQUE INDEX IF NOT EXISTS idx_projects_path_unique ON projects(path);
            CREATE INDEX IF NOT EXISTS idx_scans_project_id ON scans(project_id);
            CREATE INDEX IF NOT EXISTS idx_findings_scan_id ON findings(scan_id);
            """
        )


def create_project(db_path: str | Path | None, name: str, path: str) -> dict:
    now = _now()
    try:
        with get_connection(db_path) as connection:
            cursor = connection.execute(
                "INSERT INTO projects (name, path, created_at, updated_at) VALUES (?, ?, ?, ?)",
                (name, path, now, now),
            )
            project_id = cursor.lastrowid
    except sqlite3.IntegrityError as exc:
        if "idx_projects_path_unique" in str(exc) or "projects.path" in str(exc):
            raise ValueError("project path already exists") from exc
        raise
    return get_project(db_path, project_id) or {}


def list_projects(db_path: str | Path | None = None) -> list[dict]:
    with get_connection(db_path) as connection:
        rows = connection.execute("SELECT * FROM projects ORDER BY created_at DESC, id DESC").fetchall()
    return [_row_to_dict(row) for row in rows]


def get_project(db_path: str | Path | None, project_id: int) -> dict | None:
    with get_connection(db_path) as connection:
        row = connection.execute("SELECT * FROM projects WHERE id = ?", (project_id,)).fetchone()
    return _row_to_dict(row) if row else None


def delete_project(db_path: str | Path | None, project_id: int) -> bool:
    with get_connection(db_path) as connection:
        cursor = connection.execute("DELETE FROM projects WHERE id = ?", (project_id,))
        return cursor.rowcount > 0


def create_scan(db_path: str | Path | None, project_id: int) -> dict:
    started_at = _now()
    with get_connection(db_path) as connection:
        cursor = connection.execute(
            "INSERT INTO scans (project_id, started_at, status, summary_json) VALUES (?, ?, ?, ?)",
            (project_id, started_at, "running", "{}"),
        )
        scan_id = cursor.lastrowid
    return get_scan(db_path, scan_id) or {}


def finish_scan(
    db_path: str | Path | None,
    scan_id: int,
    status: str,
    score: int,
    summary_json: dict[str, Any],
) -> dict | None:
    finished_at = _now()
    with get_connection(db_path) as connection:
        connection.execute(
            "UPDATE scans SET finished_at = ?, status = ?, score = ?, summary_json = ? WHERE id = ?",
            (finished_at, status, score, json.dumps(summary_json, ensure_ascii=False), scan_id),
        )
    return get_scan(db_path, scan_id)


def list_scans_for_project(db_path: str | Path | None, project_id: int) -> list[dict]:
    with get_connection(db_path) as connection:
        rows = connection.execute(
            "SELECT * FROM scans WHERE project_id = ? ORDER BY started_at DESC, id DESC",
            (project_id,),
        ).fetchall()
    return [_scan_row_to_dict(row) for row in rows]


def get_scan(db_path: str | Path | None, scan_id: int) -> dict | None:
    with get_connection(db_path) as connection:
        row = connection.execute("SELECT * FROM scans WHERE id = ?", (scan_id,)).fetchone()
    return _scan_row_to_dict(row) if row else None


def create_finding(db_path: str | Path | None, scan_id: int, finding: dict) -> dict:
    created_at = _now()
    with get_connection(db_path) as connection:
        cursor = connection.execute(
            """
            INSERT INTO findings (scan_id, rule_id, severity, title, message, path, recommendation, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                scan_id,
                finding["rule_id"],
                finding["severity"],
                finding["title"],
                finding["message"],
                finding.get("path", ""),
                finding["recommendation"],
                created_at,
            ),
        )
        row = connection.execute("SELECT * FROM findings WHERE id = ?", (cursor.lastrowid,)).fetchone()
    return _row_to_dict(row)


def list_findings_for_scan(db_path: str | Path | None, scan_id: int) -> list[dict]:
    with get_connection(db_path) as connection:
        rows = connection.execute(
            "SELECT * FROM findings WHERE scan_id = ? ORDER BY severity, rule_id, id",
            (scan_id,),
        ).fetchall()
    return [_row_to_dict(row) for row in rows]


def summary(db_path: str | Path | None = None) -> dict[str, Any]:
    with get_connection(db_path) as connection:
        project_count = connection.execute("SELECT COUNT(*) AS count FROM projects").fetchone()["count"]
        scan_count = connection.execute("SELECT COUNT(*) AS count FROM scans").fetchone()["count"]
        avg_score_row = connection.execute("SELECT AVG(score) AS average_score FROM scans WHERE score IS NOT NULL").fetchone()
        recent_row = connection.execute("SELECT * FROM scans ORDER BY started_at DESC, id DESC LIMIT 1").fetchone()
    return {
        "project_count": project_count,
        "scan_count": scan_count,
        "average_score": avg_score_row["average_score"] if avg_score_row else None,
        "recent_scan": _scan_row_to_dict(recent_row) if recent_row else None,
    }


def _scan_row_to_dict(row: sqlite3.Row | None) -> dict:
    if row is None:
        return {}
    data = _row_to_dict(row)
    data["summary_json"] = json.loads(data.get("summary_json") or "{}")
    return data


def _row_to_dict(row: sqlite3.Row) -> dict:
    return dict(row)


def _now() -> str:
    return datetime.now(UTC).isoformat()
