"""GPT 导入服务 - 解析和导入 ChatGPT 对话"""

from sqlalchemy.orm import Session
from app.models.conversation import Conversation
from app.models.message import Message
from app.schemas.import_data import ChatGPTImportRequest, ManualImportRequest


def parse_chatgpt_content(content: str) -> list[dict]:
    """解析 ChatGPT 导出的内容

    V1.1 阶段使用简单解析，后续支持更多格式。
    """
    messages = []
    lines = content.strip().split("\n")

    current_role = None
    current_content = []

    for line in lines:
        if line.startswith("User:"):
            if current_role and current_content:
                messages.append({
                    "role": current_role,
                    "content": "\n".join(current_content).strip(),
                })
            current_role = "user"
            current_content = [line[5:].strip()]
        elif line.startswith("Assistant:"):
            if current_role and current_content:
                messages.append({
                    "role": current_role,
                    "content": "\n".join(current_content).strip(),
                })
            current_role = "assistant"
            current_content = [line[10:].strip()]
        elif current_role:
            current_content.append(line)

    if current_role and current_content:
        messages.append({
            "role": current_role,
            "content": "\n".join(current_content).strip(),
        })

    return messages


def import_chatgpt(db: Session, data: ChatGPTImportRequest, user_id: int, workspace_id: int) -> Conversation:
    """导入 ChatGPT 对话"""
    # 解析内容
    messages = parse_chatgpt_content(data.content)

    # 创建对话
    conversation = Conversation(
        workspace_id=workspace_id,
        title="ChatGPT 导入对话",
        source="chatgpt_web",
        created_by=user_id,
    )
    db.add(conversation)
    db.flush()

    # 创建消息
    for msg_data in messages:
        message = Message(
            conversation_id=conversation.id,
            role=msg_data["role"],
            content=msg_data["content"],
            message_type="text",
        )
        db.add(message)

    db.commit()
    db.refresh(conversation)
    return conversation


def import_manual(db: Session, data: ManualImportRequest, user_id: int) -> Conversation:
    """手动导入对话"""
    # 创建对话
    conversation = Conversation(
        workspace_id=data.workspace_id,
        title=data.title,
        source="manual_import",
        created_by=user_id,
    )
    db.add(conversation)
    db.flush()

    # 创建消息（将内容作为用户消息）
    message = Message(
        conversation_id=conversation.id,
        role="user",
        content=data.content,
        message_type="text",
    )
    db.add(message)

    db.commit()
    db.refresh(conversation)
    return conversation
