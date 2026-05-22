from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.issue import Issue
from app.models.task import Task
from app.schemas.issue import IssueResponse
from app.schemas.task import TaskResponse
from app.utils.activity_log import append_activity_log
from app.routers.deps import get_current_user

router = APIRouter(tags=["备注"])


class NoteRequest(BaseModel):
    details: str


@router.post("/api/v1/workspaces/{workspace_id}/issues/{issue_id}/notes", response_model=IssueResponse)
def add_issue_note(
    workspace_id: int,
    issue_id: int,
    data: NoteRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    issue = db.query(Issue).filter(Issue.id == issue_id, Issue.workspace_id == workspace_id).first()
    if not issue:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="问题不存在")
    issue.activity_log = append_activity_log(
        issue.activity_log, current_user.id, current_user.username, "note", data.details,
    )
    issue.version += 1
    db.commit()
    db.refresh(issue)
    return issue


@router.post("/api/v1/workspaces/{workspace_id}/issues/{issue_id}/tasks/{task_id}/notes", response_model=TaskResponse)
def add_task_note(
    workspace_id: int,
    issue_id: int,
    task_id: int,
    data: NoteRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    task = db.query(Task).filter(Task.id == task_id, Task.issue_id == issue_id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="任务不存在")
    task.activity_log = append_activity_log(
        task.activity_log, current_user.id, current_user.username, "note", data.details,
    )
    task.version += 1
    db.commit()
    db.refresh(task)
    return task
