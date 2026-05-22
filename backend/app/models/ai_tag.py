from sqlalchemy import Column, BigInteger, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from app.database import Base


class AITag(Base):
    __tablename__ = "ai_tags"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    ai_tool = Column(String(50), nullable=False)
    workspace_id = Column(BigInteger, ForeignKey("workspaces.id"), nullable=False)
    tags = Column(JSONB, nullable=False, default=dict)
    stats = Column(JSONB, nullable=False, default=dict)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        UniqueConstraint("ai_tool", "workspace_id", name="uq_ai_tags_tool_workspace"),
    )
