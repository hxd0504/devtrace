from pydantic import BaseModel, Field
from datetime import datetime


class IssueCreate(BaseModel):
    title: str = Field(..., max_length=200)
    description: str | None = None
    assignee_name: str | None = None
    executor_name: str | None = None
    executor_type: str | None = None
    executor_note: str | None = None
    related_files: list[dict] = []
    evidence_note: str | None = None


class IssueUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    assignee_name: str | None = None
    executor_name: str | None = None
    executor_type: str | None = None
    executor_note: str | None = None
    related_files: list[dict] | None = None
    evidence_note: str | None = None
    version: int


class IssueResponse(BaseModel):
    id: int
    workspace_id: int
    title: str
    description: str | None
    status: str
    creator_id: int
    assignee_name: str | None
    executor_name: str | None
    executor_type: str | None
    executor_note: str | None
    related_files: list[dict]
    evidence_note: str | None
    root_cause: str | None
    failed_attempts: str | None
    final_solution: str | None
    reusable: bool
    tags: list[str]
    activity_log: list[dict]
    version: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class StatusChangeRequest(BaseModel):
    status: str
    version: int
    details: str | None = None


class ArchiveRequest(BaseModel):
    root_cause: str
    failed_attempts: str
    final_solution: str
    reusable: bool
    tags: list[str] = []
    version: int
