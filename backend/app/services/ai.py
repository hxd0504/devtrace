"""AI 服务 - 任务草稿生成和执行体推荐

V1.1 阶段使用 Mock 数据，后续接入真实 AI。
"""

from app.schemas.task import TaskDraftResponse
from app.schemas.executor import ExecutorRecommendation


def generate_task_draft(intent: str, workspace_id: int, issue_id: int, context: dict | None = None) -> TaskDraftResponse:
    """根据用户意图和上下文生成任务草稿

    V1.1 阶段返回 Mock 数据，后续接入真实 AI 模型。
    """
    # Mock 实现：根据意图关键词生成不同草稿
    title = f"任务: {intent[:50]}" if len(intent) > 50 else f"任务: {intent}"

    # 根据意图推断执行类型
    executor_type = "ai_window"
    executor_name = "Claude Code 窗口A"

    if any(keyword in intent.lower() for keyword in ["docker", "部署", "容器"]):
        tags = ["Docker", "部署"]
        risk_level = "medium"
    elif any(keyword in intent.lower() for keyword in ["api", "接口", "调试"]):
        tags = ["API", "调试"]
        risk_level = "low"
    elif any(keyword in intent.lower() for keyword in ["数据库", "sql", "迁移"]):
        tags = ["数据库", "迁移"]
        risk_level = "high"
    else:
        tags = ["开发"]
        risk_level = "low"

    return TaskDraftResponse(
        title=title,
        description=f"根据意图「{intent}」自动生成的任务描述。请根据实际情况调整。",
        executor_type=executor_type,
        executor_name=executor_name,
        owner_name="admin",
        evidence_summary="从上下文自动提取的证据摘要",
        acceptance_criteria="1. 功能实现正确\n2. 无明显 bug\n3. 代码风格符合规范",
        risk_level=risk_level,
        tags=tags,
    )


def get_executor_recommendations(workspace_id: int) -> list[ExecutorRecommendation]:
    """获取执行体推荐列表

    V1.1 阶段返回静态列表，后续基于历史数据推荐。
    """
    return [
        ExecutorRecommendation(name="Claude Code 窗口A", type="ai_window", score=0.95),
        ExecutorRecommendation(name="MiMo", type="ai_window", score=0.88),
        ExecutorRecommendation(name="Claude Code 窗口B", type="ai_window", score=0.82),
        ExecutorRecommendation(name="admin", type="human", score=0.70),
    ]
