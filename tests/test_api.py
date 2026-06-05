from fastapi.testclient import TestClient

from oss_quality_dashboard.api import create_app


def test_health_returns_ok(tmp_path):
    app = create_app(tmp_path / "test.sqlite")
    with TestClient(app) as client:
        response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "app": "oss-quality-dashboard"}


def test_post_projects_creates_project(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    app = create_app(tmp_path / "test.sqlite")
    with TestClient(app) as client:
        response = client.post("/api/projects", json={"name": "repo", "path": str(repo)})

    assert response.status_code == 201
    assert response.json()["name"] == "repo"


def test_post_projects_rejects_missing_path(tmp_path):
    app = create_app(tmp_path / "test.sqlite")
    with TestClient(app) as client:
        response = client.post("/api/projects", json={"name": "missing", "path": str(tmp_path / "missing")})

    assert response.status_code == 400


def test_post_projects_rejects_duplicate_path(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    app = create_app(tmp_path / "test.sqlite")
    with TestClient(app) as client:
        first = client.post("/api/projects", json={"name": "repo", "path": str(repo)})
        second = client.post("/api/projects", json={"name": "repo again", "path": str(repo)})

    assert first.status_code == 201
    assert second.status_code == 409
    assert second.json()["detail"] == "project path already exists"


def test_scan_endpoint_creates_scan_and_get_scan_returns_findings(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "README.md").write_text("usage only", encoding="utf-8")
    app = create_app(tmp_path / "test.sqlite")

    with TestClient(app) as client:
        project_response = client.post("/api/projects", json={"name": "repo", "path": str(repo)})
        project_id = project_response.json()["id"]
        scan_response = client.post(f"/api/projects/{project_id}/scan")
        scan_id = scan_response.json()["scan"]["id"]
        get_response = client.get(f"/api/scans/{scan_id}")

    assert scan_response.status_code == 200
    assert scan_response.json()["scan"]["status"] == "finished"
    assert get_response.status_code == 200
    assert get_response.json()["findings"]


def test_report_endpoint_returns_markdown(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    app = create_app(tmp_path / "test.sqlite")

    with TestClient(app) as client:
        project_id = client.post("/api/projects", json={"name": "repo", "path": str(repo)}).json()["id"]
        scan_id = client.post(f"/api/projects/{project_id}/scan").json()["scan"]["id"]
        response = client.get(f"/api/scans/{scan_id}/report.md")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/markdown")
    assert "# OSS Quality Report" in response.text


def test_static_index_can_be_served(tmp_path):
    app = create_app(tmp_path / "test.sqlite")
    with TestClient(app) as client:
        response = client.get("/")

    assert response.status_code == 200
    assert "OSS Quality Dashboard" in response.text
