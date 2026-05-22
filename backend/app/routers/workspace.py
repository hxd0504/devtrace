from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.workspace import Workspace
from app.schemas.workspace import WorkspaceCreate, WorkspaceResponse, WorkspaceListResponse
from app.services.workspace import create_workspace, get_workspace, list_workspaces
from app.routers.deps import get_current_user

router = APIRouter(prefix="/api/v1/workspaces", tags=["项目空间"])


@router.get("", response_model=WorkspaceListResponse)
def list_workspace(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    items = list_workspaces(db, current_user.id)
    return WorkspaceListResponse(items=items)


@router.post("", response_model=WorkspaceResponse, status_code=status.HTTP_201_CREATED)
def create(
    data: WorkspaceCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return create_workspace(db, data, current_user.id)


@router.get("/{workspace_id}", response_model=WorkspaceResponse)
def get(
    workspace_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    workspace = get_workspace(db, workspace_id)
    if not workspace:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="项目空间不存在")
    return workspace
