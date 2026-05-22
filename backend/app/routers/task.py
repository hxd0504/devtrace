from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.services.task import create_task, get_task, list_tasks, update_task
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse, TaskStatusChangeRequest
from app.utils.state_machine import can_transition_task
from app.utils.activity_log import append_activity_log
from app.routers.deps import get_current_user

router = APIRouter(prefix="/api/v1/workspaces/{workspace_id}/issues/{issue_id}/tasks", tags=["任务管理"])


@router.get("", response_model=list[TaskResponse])
def list_task(
    workspace_id: int,
    issue_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return list_tasks(db, issue_id)


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create(
    workspace_id: int,
    issue_id: int,
    data: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return create_task(db, data, issue_id, current_user.id, current_user.username)


@router.put("/{task_id}", response_model=TaskResponse)
def update(
    workspace_id: int,
    issue_id: int,
    task_id: int,
    data: TaskUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    task = get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="任务不存在")
    try:
        return update_task(db, task, data, current_user.id, current_user.username)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.put("/{task_id}/status", response_model=TaskResponse)
def change_status(
    workspace_id: int,
    issue_id: int,
    task_id: int,
    data: TaskStatusChangeRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    task = get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="任务不存在")
    if task.version != data.version:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="版本冲突，请刷新后重试")
    if not can_transition_task(task.status, data.status):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"不允许从 {task.status} 流转到 {data.status}")
    old_status = task.status
    task.status = data.status
    task.version += 1
    task.activity_log = append_activity_log(
        task.activity_log, current_user.id, current_user.username, "status_change",
        data.details, from_status=old_status, to_status=data.status,
    )
    db.commit()
    db.refresh(task)
    return task
