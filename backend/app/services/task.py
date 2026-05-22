from sqlalchemy.orm import Session
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate
from app.utils.activity_log import append_activity_log


def create_task(db: Session, data: TaskCreate, issue_id: int, user_id: int, username: str) -> Task:
    task = Task(**data.model_dump(), issue_id=issue_id)
    task.activity_log = append_activity_log([], user_id, username, "created", "创建任务")
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def get_task(db: Session, task_id: int) -> Task | None:
    return db.query(Task).filter(Task.id == task_id).first()


def list_tasks(db: Session, issue_id: int) -> list[Task]:
    return db.query(Task).filter(Task.issue_id == issue_id).order_by(Task.created_at.desc()).all()


def update_task(db: Session, task: Task, data: TaskUpdate, user_id: int, username: str) -> Task:
    if task.version != data.version:
        raise ValueError("版本冲突，请刷新后重试")
    for key, value in data.model_dump(exclude={"version"}).items():
        if value is not None:
            setattr(task, key, value)
    task.version += 1
    task.activity_log = append_activity_log(
        task.activity_log, user_id, username, "update", "更新任务信息"
    )
    db.commit()
    db.refresh(task)
    return task
