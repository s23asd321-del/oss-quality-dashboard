import sqlite3

from oss_quality_dashboard import db
from oss_quality_dashboard.rules import make_finding


def test_init_db_creates_tables(tmp_path):
    db_path = tmp_path / "test.sqlite"
    db.init_db(db_path)

    connection = sqlite3.connect(db_path)
    rows = connection.execute("SELECT name FROM sqlite_master WHERE type = 'table'").fetchall()
    table_names = {row[0] for row in rows}

    assert {"projects", "scans", "findings"}.issubset(table_names)


def test_create_list_get_delete_project(tmp_path):
    db_path = tmp_path / "test.sqlite"
    repo = tmp_path / "repo"
    repo.mkdir()
    db.init_db(db_path)

    project = db.create_project(db_path, "repo", str(repo))

    assert project["id"] == 1
    assert db.get_project(db_path, project["id"])["name"] == "repo"
    assert len(db.list_projects(db_path)) == 1
    assert db.delete_project(db_path, project["id"]) is True
    assert db.get_project(db_path, project["id"]) is None


def test_create_project_rejects_duplicate_path(tmp_path):
    db_path = tmp_path / "test.sqlite"
    repo = tmp_path / "repo"
    repo.mkdir()
    db.init_db(db_path)
    db.create_project(db_path, "repo", str(repo))

    try:
        db.create_project(db_path, "repo again", str(repo))
    except ValueError as exc:
        assert "project path already exists" in str(exc)
    else:
        raise AssertionError("duplicate project path should fail")


def test_create_scan_and_findings(tmp_path):
    db_path = tmp_path / "test.sqlite"
    repo = tmp_path / "repo"
    repo.mkdir()
    db.init_db(db_path)
    project = db.create_project(db_path, "repo", str(repo))

    scan = db.create_scan(db_path, project["id"])
    finding = db.create_finding(db_path, scan["id"], make_finding("R001_README_MISSING", "README.md"))
    finished = db.finish_scan(db_path, scan["id"], "finished", 90, {"score": 90, "grade": "strong"})

    assert finished["status"] == "finished"
    assert finding["rule_id"] == "R001_README_MISSING"
    assert db.list_findings_for_scan(db_path, scan["id"])[0]["path"] == "README.md"
    assert db.summary(db_path)["scan_count"] == 1
