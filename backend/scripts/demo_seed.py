"""展示演示种子数据脚本

数据更真实、更像实际工作流，用于项目展示。

使用方法:
    cd backend
    python -m scripts.demo_seed
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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
            "description": "DevTrace 平台的开发和维护，包括前后端开发、数据库设计、部署配置等",
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
    """创建示例问题（覆盖不同场景）"""
    issues_data = [
        # Docker 相关问题 - archived
        {
            "workspace_id": workspace_id,
            "title": "Docker 镜像拉取失败",
            "description": "启动 vLLM 服务时，docker pull 长时间卡住或超时",
            "status": "archived",
            "creator_id": creator_id,
            "assignee_name": "admin",
            "executor_name": "Claude Code 窗口A",
            "executor_type": "ai_window",
            "executor_note": "负责 Docker 环境配置",
            "related_files": [
                {"name": "docker-compose.yml", "path": "/docker/docker-compose.yml", "note": "Docker Compose 配置文件"},
                {"name": ".env", "path": "/docker/.env", "note": "环境变量配置"},
            ],
            "evidence_note": "docker pull 超时，网络代理配置异常",
            "root_cause": "VPN/镜像源/网络代理配置异常",
            "failed_attempts": "重启Docker、更换网络、清理缓存",
            "final_solution": "配置国内镜像源并固定代理规则",
            "reusable": True,
            "tags": ["Docker", "vLLM", "环境配置"],
        },
        # LaTeX 相关问题 - resolved
        {
            "workspace_id": workspace_id,
            "title": "LaTeX 编译错误",
            "description": "论文编译时出现字体缺失错误",
            "status": "resolved",
            "creator_id": creator_id,
            "executor_name": "MiMo",
            "executor_type": "ai_window",
        },
        # API 调试问题 - in_progress
        {
            "workspace_id": workspace_id,
            "title": "FastAPI 接口返回 422",
            "description": "创建问题接口返回 422 Unprocessable Entity",
            "status": "in_progress",
            "creator_id": creator_id,
            "executor_name": "Claude Code 窗口B",
            "executor_type": "ai_window",
        },
        # 代码报错问题 - open
        {
            "workspace_id": workspace_id,
            "title": "SQLAlchemy 连接池耗尽",
            "description": "高并发时数据库连接池耗尽",
            "status": "open",
            "creator_id": creator_id,
        },
        # AI 协作交接问题 - open
        {
            "workspace_id": workspace_id,
            "title": "前端组件状态管理混乱",
            "description": "多个组件同时修改状态导致数据不一致",
            "status": "open",
            "creator_id": creator_id,
            "executor_name": "Claude Code 窗口A",
            "executor_type": "ai_window",
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

        # 为 archived 问题添加完整的 activity_log
        if data["status"] == "archived":
            activity_log = [
                {
                    "timestamp": "2026-05-20T10:00:00Z",
                    "user_id": creator_id,
                    "username": "admin",
                    "action": "created",
                    "details": "创建问题",
                },
                {
                    "timestamp": "2026-05-20T10:30:00Z",
                    "user_id": creator_id,
                    "username": "admin",
                    "action": "status_change",
                    "from_status": "open",
                    "to_status": "in_progress",
                    "details": "开始处理",
                },
                {
                    "timestamp": "2026-05-20T14:00:00Z",
                    "user_id": creator_id,
                    "username": "admin",
                    "action": "note",
                    "details": "已检查代理设置，发现配置错误",
                },
                {
                    "timestamp": "2026-05-20T16:00:00Z",
                    "user_id": creator_id,
                    "username": "admin",
                    "action": "status_change",
                    "from_status": "in_progress",
                    "to_status": "resolved",
                    "details": "问题已解决",
                },
                {
                    "timestamp": "2026-05-21T09:00:00Z",
                    "user_id": creator_id,
                    "username": "admin",
                    "action": "archived",
                    "details": "问题已归档",
                },
            ]
            data.pop("status")  # 从 data 中移除，单独设置
            issue = Issue(**data, status="archived")
            issue.activity_log = activity_log
        else:
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
    """创建示例任务（每个问题下 1-3 个任务）"""
    tasks_data = [
        # Docker 问题的任务
        {
            "issue_id": issues[0].id,
            "title": "检查网络配置",
            "description": "检查代理和镜像源配置",
            "status": "done",
            "executor_name": "Claude Code 窗口A",
            "executor_type": "ai_window",
            "activity_log": [
                {
                    "timestamp": "2026-05-20T11:00:00Z",
                    "user_id": creator_id,
                    "username": "admin",
                    "action": "status_change",
                    "from_status": "todo",
                    "to_status": "doing",
                    "details": "开始检查",
                },
                {
                    "timestamp": "2026-05-20T13:00:00Z",
                    "user_id": creator_id,
                    "username": "admin",
                    "action": "status_change",
                    "from_status": "doing",
                    "to_status": "done",
                    "details": "检查完成，发现代理配置错误",
                },
            ],
        },
        {
            "issue_id": issues[0].id,
            "title": "配置镜像源",
            "description": "配置国内 Docker 镜像源",
            "status": "done",
            "executor_name": "Claude Code 窗口A",
            "executor_type": "ai_window",
        },
        # LaTeX 问题的任务
        {
            "issue_id": issues[1].id,
            "title": "安装缺失字体",
            "description": "安装 LaTeX 编译所需的字体",
            "status": "done",
            "executor_name": "MiMo",
            "executor_type": "ai_window",
        },
        # API 问题的任务
        {
            "issue_id": issues[2].id,
            "title": "检查请求参数",
            "description": "检查 API 请求参数是否符合 Schema",
            "status": "doing",
            "executor_name": "Claude Code 窗口B",
            "executor_type": "ai_window",
        },
        {
            "issue_id": issues[2].id,
            "title": "查看错误日志",
            "description": "查看 FastAPI 的错误日志",
            "status": "todo",
            "executor_name": "Claude Code 窗口B",
            "executor_type": "ai_window",
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

        activity_log = data.pop("activity_log", None)
        task = Task(**data)
        if activity_log:
            task.activity_log = activity_log
        else:
            task.activity_log = append_activity_log(
                [], creator_id, "admin", "created", "创建任务"
            )
        db.add(task)
        db.commit()
        db.refresh(task)
        print(f"创建任务: {task.title}，状态: {task.status}，ID: {task.id}")


def main():
    print("=" * 50)
    print("DevTrace 演示种子数据初始化")
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
    print("演示种子数据初始化完成！")
    print("=" * 50)


if __name__ == "__main__":
    main()
