from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.conversation import ConversationResponse
from app.schemas.import_data import ChatGPTImportRequest, ManualImportRequest
from app.services.import_data import import_chatgpt, import_manual
from app.routers.deps import get_current_user

router = APIRouter(prefix="/api/v1/import", tags=["导入"])


@router.post("/chatgpt", response_model=ConversationResponse, status_code=status.HTTP_201_CREATED)
def import_chatgpt_conversation(
    data: ChatGPTImportRequest,
    workspace_id: int = Query(..., description="项目空间 ID"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return import_chatgpt(db, data, current_user.id, workspace_id)


@router.post("/manual", response_model=ConversationResponse, status_code=status.HTTP_201_CREATED)
def import_manual_conversation(
    data: ManualImportRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return import_manual(db, data, current_user.id)
