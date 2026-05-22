from pydantic import BaseModel, Field
from datetime import datetime


class TaskCreate(BaseModel):
    title: str = Field(..., max_length=200)
    description: str | None = None
    owner_name: str | None = None
    executor_name: str | None = None
    executor_type: str | None = None
    executor_note: str | None = None
    related_files: list[dict] = []
    evidence_source: str | None = None
    evidence_summary: str | None = None
    acceptance_criteria: str | None = None
    risk_level: str | None = None


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    owner_name: str | None = None
    executor_name: str | None = None
    executor_type: str | None = None
    executor_note: str | None = None
    related_files: list[dict] | None = None
    evidence_source: str | None = None
    evidence_summary: str | None = None
    acceptance_criteria: str | None = None
    risk_level: str | None = None
    version: int


class TaskResponse(BaseModel):
    id: int
    issue_id: int
    title: str
    description: str | None
    status: str
    owner_name: str | None
    executor_name: str | None
    executor_type: str | None
    executor_note: str | None
    related_files: list[dict]
    evidence_source: str | None
    evidence_summary: str | None
    acceptance_criteria: str | None
    risk_level: str | None
    activity_log: list[dict]
    version: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TaskStatusChangeRequest(BaseModel):
    status: str
    version: int
    details: str | None = None


class TaskDraftRequest(BaseModel):
    intent: str
    workspace_id: int
    issue_id: int
    context: dict | None = None


class TaskDraftResponse(BaseModel):
    title: str
    description: str | None = None
    executor_type: str | None = None
    executor_name: str | None = None
    owner_name: str | None = None
    evidence_summary: str | None = None
    acceptance_criteria: str | None = None
    risk_level: str | None = None
    tags: list[str] = []
