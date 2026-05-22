from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.dispatch import (
    AITagResponse, AITagUpdate,
    DispatchRequest, DispatchResponse, DispatchRecordResponse,
)
from app.services.dispatch import (
    get_ai_tags, update_ai_tag,
    dispatch_task, get_dispatch_records,
)
from app.routers.deps import get_current_user

router = APIRouter(prefix="/api/v1", tags=["AI 调度"])


@router.get("/ai-tags", response_model=list[AITagResponse])
def list_ai_tags(
    workspace_id: int = Query(..., description="项目空间 ID"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_ai_tags(db, workspace_id)


@router.put("/ai-tags/{ai_tool}", response_model=AITagResponse)
def update_tag(
    ai_tool: str,
    data: AITagUpdate,
    workspace_id: int = Query(..., description="项目空间 ID"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return update_ai_tag(db, ai_tool, workspace_id, data)


@router.post("/dispatch", response_model=DispatchResponse, status_code=status.HTTP_201_CREATED)
def create_dispatch(
    data: DispatchRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        return dispatch_task(db, data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/dispatch/records", response_model=list[DispatchRecordResponse])
def list_dispatch_records(
    task_id: int | None = Query(None, description="任务 ID"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_dispatch_records(db, task_id)
