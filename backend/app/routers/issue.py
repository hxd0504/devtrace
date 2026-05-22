from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.services.issue import create_issue, get_issue, list_issues, update_issue
from app.schemas.issue import IssueCreate, IssueUpdate, IssueResponse, StatusChangeRequest, ArchiveRequest
from app.utils.state_machine import can_transition_issue, validate_archive_fields
from app.utils.activity_log import append_activity_log
from app.routers.deps import get_current_user

router = APIRouter(prefix="/api/v1/workspaces/{workspace_id}/issues", tags=["问题管理"])


@router.get("", response_model=list[IssueResponse])
def list_issue(
    workspace_id: int,
    status: str | None = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return list_issues(db, workspace_id, status)


@router.post("", response_model=IssueResponse, status_code=status.HTTP_201_CREATED)
def create(
    workspace_id: int,
    data: IssueCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return create_issue(db, data, workspace_id, current_user.id, current_user.username)


@router.get("/{issue_id}", response_model=IssueResponse)
def get(
    workspace_id: int,
    issue_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    issue = get_issue(db, issue_id)
    if not issue:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="问题不存在")
    return issue


@router.put("/{issue_id}", response_model=IssueResponse)
def update(
    workspace_id: int,
    issue_id: int,
    data: IssueUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    issue = get_issue(db, issue_id)
    if not issue:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="问题不存在")
    try:
        return update_issue(db, issue, data, current_user.id, current_user.username)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.put("/{issue_id}/status", response_model=IssueResponse)
def change_status(
    workspace_id: int,
    issue_id: int,
    data: StatusChangeRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    issue = get_issue(db, issue_id)
    if not issue:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="问题不存在")
    if issue.version != data.version:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="版本冲突，请刷新后重试")
    if not can_transition_issue(issue.status, data.status):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"不允许从 {issue.status} 流转到 {data.status}")
    old_status = issue.status
    issue.status = data.status
    issue.version += 1
    issue.activity_log = append_activity_log(
        issue.activity_log, current_user.id, current_user.username, "status_change",
        data.details, from_status=old_status, to_status=data.status,
    )
    db.commit()
    db.refresh(issue)
    return issue


@router.post("/{issue_id}/archive", response_model=IssueResponse)
def archive(
    workspace_id: int,
    issue_id: int,
    data: ArchiveRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    issue = get_issue(db, issue_id)
    if not issue:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="问题不存在")
    if issue.status != "resolved":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="只有 resolved 状态的问题才能归档")
    errors = validate_archive_fields(data.model_dump())
    if errors:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=", ".join(errors))
    if issue.version != data.version:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="版本冲突，请刷新后重试")
    issue.root_cause = data.root_cause
    issue.failed_attempts = data.failed_attempts
    issue.final_solution = data.final_solution
    issue.reusable = data.reusable
    issue.tags = data.tags
    issue.status = "archived"
    issue.version += 1
    issue.activity_log = append_activity_log(
        issue.activity_log, current_user.id, current_user.username, "archived", "问题已归档",
    )
    db.commit()
    db.refresh(issue)
    return issue
