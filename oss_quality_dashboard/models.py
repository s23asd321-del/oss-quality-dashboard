"""Pydantic models used by the HTTP API."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class ProjectCreate(BaseModel):
    name: str = Field(min_length=1, max_length=160)
    path: str = Field(min_length=1)


class ProjectUpdate(BaseModel):
    name: str = Field(min_length=1, max_length=160)


class ProjectOut(BaseModel):
    id: int
    name: str
    path: str
    created_at: str
    updated_at: str


class FindingOut(BaseModel):
    id: int | None = None
    scan_id: int | None = None
    rule_id: str
    severity: str
    title: str
    message: str
    path: str
    recommendation: str
    created_at: str | None = None


class ScanOut(BaseModel):
    id: int
    project_id: int
    started_at: str
    finished_at: str | None = None
    status: str
    score: int | None = None
    summary_json: dict[str, Any]


class ScanWithFindings(BaseModel):
    scan: ScanOut
    findings: list[FindingOut]

