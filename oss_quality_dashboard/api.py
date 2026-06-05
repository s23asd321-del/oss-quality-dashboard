"""FastAPI application factory and endpoints."""

from __future__ import annotations

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import FileResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles

from . import db
from .models import ProjectCreate
from .reports import build_summary, generate_markdown_report
from .scanner import scan_project
from .scoring import calculate_score
from .settings import APP_NAME, DEFAULT_DATABASE_PATH

STATIC_DIR = Path(__file__).parent / "static"


def create_app(db_path: str | Path | None = None) -> FastAPI:
    database_path = Path(db_path or DEFAULT_DATABASE_PATH)

    @asynccontextmanager
    async def lifespan(application: FastAPI):
        db.init_db(application.state.db_path)
        yield

    app = FastAPI(title=APP_NAME, lifespan=lifespan)
    app.state.db_path = database_path

    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

    @app.get("/")
    def index() -> FileResponse:
        return FileResponse(STATIC_DIR / "index.html")

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok", "app": APP_NAME}

    @app.get("/api/projects")
    def list_projects() -> list[dict]:
        return db.list_projects(app.state.db_path)

    @app.post("/api/projects", status_code=201)
    def create_project(payload: ProjectCreate) -> dict:
        path = Path(payload.path).expanduser().resolve()
        if not path.exists():
            raise HTTPException(status_code=400, detail="path must exist")
        if not path.is_dir():
            raise HTTPException(status_code=400, detail="path must be a directory")
        try:
            return db.create_project(app.state.db_path, payload.name.strip(), str(path))
        except ValueError as exc:
            raise HTTPException(status_code=409, detail=str(exc)) from exc

    @app.get("/api/projects/{project_id}")
    def get_project(project_id: int) -> dict:
        project = db.get_project(app.state.db_path, project_id)
        if not project:
            raise HTTPException(status_code=404, detail="project not found")
        return project

    @app.delete("/api/projects/{project_id}")
    def delete_project(project_id: int) -> dict[str, bool]:
        deleted = db.delete_project(app.state.db_path, project_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="project not found")
        return {"deleted": True}

    @app.post("/api/projects/{project_id}/scan")
    def scan_project_endpoint(project_id: int) -> dict:
        project = db.get_project(app.state.db_path, project_id)
        if not project:
            raise HTTPException(status_code=404, detail="project not found")

        scan = db.create_scan(app.state.db_path, project_id)
        result = scan_project(project["path"])
        findings = result["findings"]
        scored = calculate_score(findings)
        summary = dict(result["summary"])
        summary.update(build_summary(findings, int(scored["score"]), str(scored["grade"])))
        finished_scan = db.finish_scan(app.state.db_path, scan["id"], "finished", int(scored["score"]), summary)
        stored_findings = [db.create_finding(app.state.db_path, scan["id"], finding) for finding in findings]
        return {"scan": finished_scan, "findings": stored_findings}

    @app.get("/api/projects/{project_id}/scans")
    def list_project_scans(project_id: int) -> list[dict]:
        if not db.get_project(app.state.db_path, project_id):
            raise HTTPException(status_code=404, detail="project not found")
        return db.list_scans_for_project(app.state.db_path, project_id)

    @app.get("/api/scans/{scan_id}")
    def get_scan(scan_id: int) -> dict:
        scan = db.get_scan(app.state.db_path, scan_id)
        if not scan:
            raise HTTPException(status_code=404, detail="scan not found")
        findings = db.list_findings_for_scan(app.state.db_path, scan_id)
        return {"scan": scan, "findings": findings}

    @app.get("/api/scans/{scan_id}/report.md")
    def get_scan_report(scan_id: int) -> Response:
        scan = db.get_scan(app.state.db_path, scan_id)
        if not scan:
            raise HTTPException(status_code=404, detail="scan not found")
        project = db.get_project(app.state.db_path, scan["project_id"])
        findings = db.list_findings_for_scan(app.state.db_path, scan_id)
        markdown = generate_markdown_report(project or {}, scan, findings)
        return PlainTextResponse(markdown, media_type="text/markdown; charset=utf-8")

    @app.get("/api/summary")
    def api_summary() -> dict:
        return db.summary(app.state.db_path)

    return app
