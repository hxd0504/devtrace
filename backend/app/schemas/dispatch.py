from pydantic import BaseModel
from datetime import datetime


class AITagResponse(BaseModel):
    id: int
    ai_tool: str
    workspace_id: int | None
    tags: dict
    stats: dict
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AITagUpdate(BaseModel):
    tags: dict | None = None
    stats: dict | None = None


class DispatchRequest(BaseModel):
    task_id: int
    task_type: str | None = None
    preferred_ai: str | None = None


class DispatchResponse(BaseModel):
    id: int
    task_id: int
    ai_tool: str
    dispatch_reason: str | None
    risk_level: str | None
    execution_prompt: str | None
    success: bool | None
    created_at: datetime

    class Config:
        from_attributes = True


class DispatchRecordResponse(DispatchResponse):
    execution_result: str | None = None
    duration_seconds: int | None = None
