from pydantic import BaseModel
from typing import Literal
from datetime import datetime


class ConversationCreate(BaseModel):
    title: str | None = None
    workspace_id: int
    source: str = "devtrace"


class ConversationResponse(BaseModel):
    id: int
    workspace_id: int
    title: str | None
    source: str
    created_by: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class MessageCreate(BaseModel):
    role: Literal["user", "assistant", "system"]
    content: str
    message_type: Literal["text", "execution_result", "knowledge_extract", "system_notify"] = "text"
    metadata: dict | None = None


class MessageResponse(BaseModel):
    id: int
    conversation_id: int
    role: str
    content: str
    message_type: str
    metadata: dict
    created_at: datetime

    class Config:
        from_attributes = True
