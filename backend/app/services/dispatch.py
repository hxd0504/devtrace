"""AI 调度服务 - 根据任务类型推荐 AI 工具"""

from sqlalchemy.orm import Session
from app.models.ai_tag import AITag
from app.models.dispatch_record import DispatchRecord
from app.models.task import Task
from app.schemas.dispatch import AITagUpdate, DispatchRequest


# 调度规则：任务类型 -> 首选 AI, 备选 AI
DISPATCH_RULES = {
    "backend": {"primary": "Claude Code", "secondary": "Codex", "reason": "代码生成能力强"},
    "frontend": {"primary": "Claude Code", "secondary": "Codex", "reason": "前端代码生成"},
    "test": {"primary": "Codex", "secondary": "Claude Code", "reason": "测试代码生成"},
    "docs": {"primary": "Claude Code", "secondary": "GPT", "reason": "文档编写"},
    "design": {"primary": "GPT", "secondary": "Claude Code", "reason": "方案设计"},
    "debug": {"primary": "Claude Code", "secondary": "Codex", "reason": "调试修复"},
}


def get_ai_tags(db: Session, workspace_id: int) -> list[AITag]:
    """获取项目空间的 AI 标签列表"""
    return db.query(AITag).filter(AITag.workspace_id == workspace_id).all()


def get_ai_tag(db: Session, ai_tool: str, workspace_id: int) -> AITag | None:
    """获取单个 AI 标签"""
    return db.query(AITag).filter(
        AITag.ai_tool == ai_tool,
        AITag.workspace_id == workspace_id,
    ).first()


def update_ai_tag(db: Session, ai_tool: str, workspace_id: int, data: AITagUpdate) -> AITag:
    """更新 AI 标签"""
    tag = get_ai_tag(db, ai_tool, workspace_id)
    if not tag:
        tag = AITag(ai_tool=ai_tool, workspace_id=workspace_id)
        db.add(tag)

    if data.tags is not None:
        tag.tags = data.tags
    if data.stats is not None:
        tag.stats = data.stats

    db.commit()
    db.refresh(tag)
    return tag


def dispatch_task(db: Session, data: DispatchRequest) -> DispatchRecord:
    """调度任务到 AI 工具

    根据任务类型和 AI 标签推荐最合适的 AI 工具。
    """
    task = db.query(Task).filter(Task.id == data.task_id).first()
    if not task:
        raise ValueError("任务不存在")

    # 确定任务类型
    task_type = data.task_type or "backend"

    # 获取调度规则
    rule = DISPATCH_RULES.get(task_type, DISPATCH_RULES["backend"])

    # 确定 AI 工具
    ai_tool = data.preferred_ai or rule["primary"]

    # 生成执行提示词（结构化模板，隔离用户输入与系统指令）
    execution_prompt = (
        f"系统指令：请根据以下任务信息完成工作。\n"
        f"--- 任务信息开始 ---\n"
        f"标题: {task.title}\n"
        f"描述: {task.description or '无'}\n"
        f"类型: {task_type}\n"
        f"执行体: {task.executor_name or '未指定'}\n"
        f"--- 任务信息结束 ---"
    )

    # 创建调度记录
    record = DispatchRecord(
        task_id=data.task_id,
        ai_tool=ai_tool,
        dispatch_reason=rule["reason"],
        risk_level="medium",
        execution_prompt=execution_prompt,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def get_dispatch_records(db: Session, task_id: int | None = None) -> list[DispatchRecord]:
    """获取调度记录"""
    query = db.query(DispatchRecord)
    if task_id:
        query = query.filter(DispatchRecord.task_id == task_id)
    return query.order_by(DispatchRecord.created_at.desc()).all()
