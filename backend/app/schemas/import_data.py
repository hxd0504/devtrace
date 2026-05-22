from pydantic import BaseModel


class ChatGPTImportRequest(BaseModel):
    url: str | None = None
    content: str


class ManualImportRequest(BaseModel):
    title: str
    content: str
    workspace_id: int
