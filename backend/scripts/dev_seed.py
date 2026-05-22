"""开发调试种子数据脚本

覆盖不同状态和边界情况，用于开发阶段调试。

使用方法:
    cd backend
    python -m scripts.dev_seed
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime
from sqlalchemy.orm import Session
from app.database import engine, SessionLocal
from app.models.user import User
from app.models.workspace import Workspace
from app.models.issue import Issue
from app.models.task import Task
from app.utils.security import hash_password
from app.utils.activity_log import append_activity_log


def create_tables():
    """创建所有表"""
    from app.database import Base
    from app.models import User, Workspace, Issue, Task
    Base.metadata.create_all(bind=engine)
    print("表创建完成")


def seed_users(db: Session):
    """创建管理员账号"""
    existing = db.query(User).filter(User.username == "admin").first()
    if existing:
        print("admin 用户已存在，跳过")
        return existing

    user = User(
        username="admin",
        password_hash=hash_password("admin123"),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    print(f"创建 admin 用户，ID: {user.id}")
    return user


def seed_workspaces(db: Session, owner_id: int):
    """创建示例项目空间"""
    workspaces_data = [
        {
            "name": "DevTrace 自身开发项目",
            "description": "DevTrace 平台的开发和维护",
            "owner_id": owner_id,
        },
        {
            "name": "Docker 环境问题",
            "description": "Docker 相关的环境配置问题",
            "owner_id": owner_id,
        },
    ]

    workspaces = []
    for data in workspaces_data:
        existing = db.query(Workspace).filter(Workspace.name == data["name"]).first()
        if existing:
            print(f"项目空间 '{data['name']}' 已存在，跳过")
            workspaces.append(existing)
            continue

        ws = Workspace(**data)
        db.add(ws)
        db.commit()
        db.refresh(ws)
        workspaces.append(ws)
        print(f"创建项目空间: {ws.name}，ID: {ws.id}")

    return workspaces


def seed_issues(db: Session, workspace_id: int, creator_id: int):
    """创建示例问题（覆盖 4 种状态）"""
    issues_data = [
        # open 状态
        {
            "workspace_id": workspace_id,
            "title": "前端路由配置问题",
            "description": "Vue Router 配置后页面无法正常跳转",
            "status": "open",
            "creator_id": creator_id,
            "executor_name": "Claude Code 窗口A",
            "executor_type": "ai_window",
        },
        # in_progress 状态
        {
            "workspace_id": workspace_id,
            "title": "API 接口文档生成",
            "description": "需要配置 Swagger UI 自动生成 API 文档",
            "status": "in_progress",
            "creator_id": creator_id,
            "executor_name": "MiMo",
            "executor_type": "ai_window",
        },
        # resolved 状态
        {
            "workspace_id": workspace_id,
            "title": "数据库迁移脚本",
            "description": "Alembic 迁移脚本配置完成",
            "status": "resolved",
            "creator_id": creator_id,
            "executor_name": "admin",
            "executor_type": "human",
        },
        # archived 状态
        {
            "workspace_id": workspace_id,
            "title": "Docker Compose 配置",
            "description": "Docker Compose 一键启动配置",
            "status": "archived",
            "creator_id": creator_id,
            "executor_name": "Claude Code 窗口B",
            "executor_type": "ai_window",
            "root_cause": "Docker Compose 文件格式错误",
            "failed_attempts": "手动启动服务、检查端口占用",
            "final_solution": "修复 docker-compose.yml 格式，添加 depends_on",
            "reusable": True,
            "tags": ["Docker", "部署"],
        },
    ]

    issues = []
    for data in issues_data:
        existing = db.query(Issue).filter(
            Issue.title == data["title"],
            Issue.workspace_id == data["workspace_id"],
        ).first()
        if existing:
            print(f"问题 '{data['title']}' 已存在，跳过")
            issues.append(existing)
            continue

        issue = Issue(**data)
        issue.activity_log = append_activity_log(
            [], creator_id, "admin", "created", "创建问题"
        )
        db.add(issue)
        db.commit()
        db.refresh(issue)
        issues.append(issue)
        print(f"创建问题: {issue.title}，状态: {issue.status}，ID: {issue.id}")

    return issues


def seed_tasks(db: Session, issues: list[Issue], creator_id: int):
    """创建示例任务（覆盖 3 种状态）"""
    tasks_data = [
        # 对应 open 问题的任务
        {
            "issue_id": issues[0].id,
            "title": "检查路由配置",
            "description": "检查 Vue Router 的路由表配置",
            "status": "todo",
            "executor_name": "Claude Code 窗口A",
            "executor_type": "ai_window",
        },
        # 对应 in_progress 问题的任务
        {
            "issue_id": issues[1].id,
            "title": "配置 Swagger",
            "description": "配置 FastAPI 的 Swagger UI",
            "status": "doing",
            "executor_name": "MiMo",
            "executor_type": "ai_window",
        },
        # 对应 resolved 问题的任务
        {
            "issue_id": issues[2].id,
            "title": "创建迁移脚本",
            "description": "使用 Alembic 创建数据库迁移脚本",
            "status": "done",
            "executor_name": "admin",
            "executor_type": "human",
        },
    ]

    for data in tasks_data:
        existing = db.query(Task).filter(
            Task.title == data["title"],
            Task.issue_id == data["issue_id"],
        ).first()
        if existing:
            print(f"任务 '{data['title']}' 已存在，跳过")
            continue

        task = Task(**data)
        task.activity_log = append_activity_log(
            [], creator_id, "admin", "created", "创建任务"
        )
        db.add(task)
        db.commit()
        db.refresh(task)
        print(f"创建任务: {task.title}，状态: {task.status}，ID: {task.id}")


def main():
    print("=" * 50)
    print("DevTrace 开发种子数据初始化")
    print("=" * 50)

    create_tables()

    db = SessionLocal()
    try:
        user = seed_users(db)
        workspaces = seed_workspaces(db, user.id)
        if workspaces:
            issues = seed_issues(db, workspaces[0].id, user.id)
            seed_tasks(db, issues, user.id)
    finally:
        db.close()

    print("=" * 50)
    print("种子数据初始化完成！")
    print("=" * 50)


if __name__ == "__main__":
    main()
