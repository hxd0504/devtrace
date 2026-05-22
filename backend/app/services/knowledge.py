"""知识沉淀服务 - 思维链管理和知识提取"""

from sqlalchemy.orm import Session
from app.models.thought_chain import ThoughtChain
from app.models.conversation import Conversation
from app.models.message import Message
from app.schemas.knowledge import ThoughtChainCreate


def _escape_like(s: str) -> str:
    """转义 LIKE 通配符"""
    return s.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")


def create_thought_chain(db: Session, data: ThoughtChainCreate) -> ThoughtChain:
    """创建思维链"""
    chain = ThoughtChain(**data.model_dump())
    db.add(chain)
    db.commit()
    db.refresh(chain)
    return chain


def get_thought_chain(db: Session, chain_id: int) -> ThoughtChain | None:
    """获取单个思维链"""
    return db.query(ThoughtChain).filter(ThoughtChain.id == chain_id).first()


def list_thought_chains(db: Session, workspace_id: int) -> list[ThoughtChain]:
    """获取项目空间的思维链列表"""
    return (
        db.query(ThoughtChain)
        .filter(ThoughtChain.workspace_id == workspace_id)
        .order_by(ThoughtChain.created_at.desc())
        .all()
    )


def search_thought_chains(db: Session, workspace_id: int, query: str) -> list[ThoughtChain]:
    """搜索思维链"""
    escaped = _escape_like(query)
    return (
        db.query(ThoughtChain)
        .filter(
            ThoughtChain.workspace_id == workspace_id,
            ThoughtChain.problem.ilike(f"%{escaped}%"),
        )
        .order_by(ThoughtChain.created_at.desc())
        .all()
    )


def extract_knowledge_from_conversation(db: Session, conversation_id: int) -> list[ThoughtChain]:
    """从对话中提取思维链

    V1.1 阶段使用 Mock 实现，后续接入真实 AI 提取。
    """
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conversation:
        raise ValueError("对话不存在")

    messages = (
        db.query(Message)
        .filter(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.asc())
        .all()
    )

    # Mock 实现：从对话中提取简单思维链
    if not messages:
        return []

    # 提取问题（使用对话标题或第一条消息）
    problem = conversation.title or messages[0].content[:100]

    # 生成思维链（Mock）
    thought_chain = []
    for i, msg in enumerate(messages[:5], 1):
        thought_chain.append({
            "step": i,
            "content": msg.content[:200],
            "role": msg.role,
        })

    # 创建思维链
    chain = ThoughtChain(
        workspace_id=conversation.workspace_id,
        problem=problem,
        thought_chain=thought_chain,
        tags=["auto_extract"],
        source="auto_extract",
    )
    db.add(chain)
    db.commit()
    db.refresh(chain)

    return [chain]
