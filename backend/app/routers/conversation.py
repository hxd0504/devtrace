from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.conversation import (
    ConversationCreate, ConversationResponse,
    MessageCreate, MessageResponse,
)
from app.services.conversation import (
    create_conversation, get_conversation, list_conversations,
    create_message, list_messages,
)
from app.routers.deps import get_current_user

router = APIRouter(prefix="/api/v1/conversations", tags=["对话"])


@router.get("", response_model=list[ConversationResponse])
def list_conversation(
    workspace_id: int = Query(..., description="项目空间 ID"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return list_conversations(db, workspace_id)


@router.post("", response_model=ConversationResponse, status_code=status.HTTP_201_CREATED)
def create(
    data: ConversationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return create_conversation(db, data, current_user.id)


@router.get("/{conversation_id}", response_model=ConversationResponse)
def get(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    conversation = get_conversation(db, conversation_id)
    if not conversation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="对话不存在")
    return conversation


@router.get("/{conversation_id}/messages", response_model=list[MessageResponse])
def list_message(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    conversation = get_conversation(db, conversation_id)
    if not conversation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="对话不存在")
    return list_messages(db, conversation_id)


@router.post("/{conversation_id}/messages", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
def create_msg(
    conversation_id: int,
    data: MessageCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    conversation = get_conversation(db, conversation_id)
    if not conversation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="对话不存在")
    return create_message(db, conversation_id, data)
