# API

All endpoints are intended for local use at `http://127.0.0.1:8000`.

## GET /health

Response:

```json
{
  "status": "ok",
  "app": "oss-quality-dashboard"
}
```

## GET /api/projects

Returns all stored projects.

Response:

```json
[
  {
    "id": 1,
    "name": "sample-good-repo",
    "path": "/Users/<redacted>/project/examples/sample-good-repo",
    "created_at": "2026-01-01T00:00:00+00:00",
    "updated_at": "2026-01-01T00:00:00+00:00"
  }
]
```

## POST /api/projects

Creates a project record. This does not automatically scan.

Request:

```json
{
  "name": "sample-good-repo",
  "path": "examples/sample-good-repo"
}
```

Response: project object.

Errors:

- `400`: path does not exist or is not a directory
- `409`: project path already exists
- `422`: invalid JSON body

## GET /api/projects/{project_id}

Returns one project.

Errors:

- `404`: project not found

## DELETE /api/projects/{project_id}

Deletes the project and related scans/findings.

Response:

```json
{
  "deleted": true
}
```

Errors:

- `404`: project not found

## POST /api/projects/{project_id}/scan

Runs a synchronous read-only scan.

Response:

```json
{
  "scan": {
    "id": 1,
    "project_id": 1,
    "started_at": "2026-01-01T00:00:00+00:00",
    "finished_at": "2026-01-01T00:00:01+00:00",
    "status": "finished",
    "score": 96,
    "summary_json": {
      "score": 96,
      "grade": "strong",
      "total_findings": 1,
      "severity_counts": {
        "error": 0,
        "warning": 0,
        "info": 1
      }
    }
  },
  "findings": []
}
```

Errors:

- `404`: project not found

## GET /api/projects/{project_id}/scans

Returns scan history for one project.

Errors:

- `404`: project not found

## GET /api/scans/{scan_id}

Returns a scan plus findings.

Errors:

- `404`: scan not found

## GET /api/scans/{scan_id}/report.md

Returns a Markdown report with media type `text/markdown`.

Errors:

- `404`: scan not found

## GET /api/summary

Returns aggregate dashboard summary.

Response:

```json
{
  "project_count": 1,
  "scan_count": 1,
  "average_score": 96.0,
  "recent_scan": {
    "id": 1,
    "project_id": 1,
    "status": "finished",
    "score": 96
  }
}
```
