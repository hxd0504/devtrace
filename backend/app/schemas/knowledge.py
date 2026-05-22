from pydantic import BaseModel
from datetime import datetime


class ThoughtChainCreate(BaseModel):
    workspace_id: int
    problem: str
    thought_chain: list[dict]
    tags: list[str] = []
    source: str = "manual"
    related_issue_ids: list[int] = []


class ThoughtChainResponse(BaseModel):
    id: int
    workspace_id: int
    problem: str
    thought_chain: list[dict]
    tags: list[str]
    source: str
    related_issue_ids: list[int]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class KnowledgeExtractRequest(BaseModel):
    conversation_id: int
