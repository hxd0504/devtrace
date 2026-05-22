from sqlalchemy import Column, BigInteger, Text, DateTime, ForeignKey, Index
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from app.database import Base


class ThoughtChain(Base):
    __tablename__ = "thought_chains"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    workspace_id = Column(BigInteger, ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False)
    problem = Column(Text, nullable=False)
    thought_chain = Column(JSONB, nullable=False, default=list)
    tags = Column(JSONB, default=list)
    source = Column(Text, default="auto_extract")
    related_issue_ids = Column(JSONB, default=list)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        Index("idx_thought_chains_workspace", "workspace_id"),
    )
