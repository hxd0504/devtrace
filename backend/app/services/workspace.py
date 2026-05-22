from sqlalchemy.orm import Session
from app.models.workspace import Workspace
from app.schemas.workspace import WorkspaceCreate


def create_workspace(db: Session, data: WorkspaceCreate, owner_id: int) -> Workspace:
    workspace = Workspace(**data.model_dump(), owner_id=owner_id)
    db.add(workspace)
    db.commit()
    db.refresh(workspace)
    return workspace


def get_workspace(db: Session, workspace_id: int) -> Workspace | None:
    return db.query(Workspace).filter(Workspace.id == workspace_id).first()


def list_workspaces(db: Session, owner_id: int) -> list[Workspace]:
    return db.query(Workspace).filter(Workspace.owner_id == owner_id).all()
