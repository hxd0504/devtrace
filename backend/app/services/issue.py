from sqlalchemy.orm import Session
from app.models.issue import Issue
from app.schemas.issue import IssueCreate, IssueUpdate
from app.utils.activity_log import append_activity_log


def create_issue(db: Session, data: IssueCreate, workspace_id: int, creator_id: int, username: str) -> Issue:
    issue = Issue(**data.model_dump(), workspace_id=workspace_id, creator_id=creator_id)
    issue.activity_log = append_activity_log([], creator_id, username, "created", "创建问题")
    db.add(issue)
    db.commit()
    db.refresh(issue)
    return issue


def get_issue(db: Session, issue_id: int) -> Issue | None:
    return db.query(Issue).filter(Issue.id == issue_id).first()


def list_issues(db: Session, workspace_id: int, status: str | None = None) -> list[Issue]:
    query = db.query(Issue).filter(Issue.workspace_id == workspace_id)
    if status:
        query = query.filter(Issue.status == status)
    return query.order_by(Issue.created_at.desc()).all()


def update_issue(db: Session, issue: Issue, data: IssueUpdate, user_id: int, username: str) -> Issue:
    if issue.version != data.version:
        raise ValueError("版本冲突，请刷新后重试")
    for key, value in data.model_dump(exclude={"version"}).items():
        if value is not None:
            setattr(issue, key, value)
    issue.version += 1
    issue.activity_log = append_activity_log(
        issue.activity_log, user_id, username, "update", "更新问题信息"
    )
    db.commit()
    db.refresh(issue)
    return issue
