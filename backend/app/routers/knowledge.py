from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.knowledge import (
    ThoughtChainCreate, ThoughtChainResponse, KnowledgeExtractRequest,
)
from app.services.knowledge import (
    create_thought_chain, get_thought_chain, list_thought_chains,
    search_thought_chains, extract_knowledge_from_conversation,
)
from app.routers.deps import get_current_user

router = APIRouter(prefix="/api/v1", tags=["知识沉淀"])


@router.get("/thought-chains", response_model=list[ThoughtChainResponse])
def list_chains(
    workspace_id: int = Query(..., description="项目空间 ID"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return list_thought_chains(db, workspace_id)


@router.post("/thought-chains", response_model=ThoughtChainResponse, status_code=status.HTTP_201_CREATED)
def create_chain(
    data: ThoughtChainCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return create_thought_chain(db, data)


@router.get("/thought-chains/search", response_model=list[ThoughtChainResponse])
def search_chains(
    workspace_id: int = Query(..., description="项目空间 ID"),
    q: str = Query(..., description="搜索关键词"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return search_thought_chains(db, workspace_id, q)


@router.post("/knowledge/extract", response_model=list[ThoughtChainResponse])
def extract_knowledge(
    data: KnowledgeExtractRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        return extract_knowledge_from_conversation(db, data.conversation_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
