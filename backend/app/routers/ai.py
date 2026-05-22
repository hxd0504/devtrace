from fastapi import APIRouter, Depends, Query
from app.models.user import User
from app.schemas.task import TaskDraftRequest, TaskDraftResponse
from app.schemas.executor import ExecutorRecommendation
from app.services.ai import generate_task_draft, get_executor_recommendations
from app.routers.deps import get_current_user

router = APIRouter(prefix="/api/v1", tags=["AI 推断"])


@router.post("/tasks/draft", response_model=TaskDraftResponse)
def create_task_draft(
    data: TaskDraftRequest,
    current_user: User = Depends(get_current_user),
):
    """根据用户意图和上下文生成任务草稿"""
    return generate_task_draft(
        intent=data.intent,
        workspace_id=data.workspace_id,
        issue_id=data.issue_id,
        context=data.context,
    )


@router.get("/executors", response_model=list[ExecutorRecommendation])
def list_executors(
    workspace_id: int = Query(..., description="项目空间 ID"),
    current_user: User = Depends(get_current_user),
):
    """获取执行体推荐列表"""
    return get_executor_recommendations(workspace_id)
