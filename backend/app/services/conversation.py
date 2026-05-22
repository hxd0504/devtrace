from sqlalchemy.orm import Session
from app.models.conversation import Conversation
from app.models.message import Message
from app.schemas.conversation import ConversationCreate, MessageCreate


def create_conversation(db: Session, data: ConversationCreate, user_id: int) -> Conversation:
    conversation = Conversation(**data.model_dump(), created_by=user_id)
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    return conversation


def get_conversation(db: Session, conversation_id: int) -> Conversation | None:
    return db.query(Conversation).filter(Conversation.id == conversation_id).first()


def list_conversations(db: Session, workspace_id: int) -> list[Conversation]:
    return (
        db.query(Conversation)
        .filter(Conversation.workspace_id == workspace_id)
        .order_by(Conversation.updated_at.desc())
        .all()
    )


def create_message(db: Session, conversation_id: int, data: MessageCreate) -> Message:
    message = Message(**data.model_dump(), conversation_id=conversation_id)
    db.add(message)
    db.commit()
    db.refresh(message)
    return message


def list_messages(db: Session, conversation_id: int) -> list[Message]:
    return (
        db.query(Message)
        .filter(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.asc())
        .all()
    )
