from sqlalchemy import Column, BigInteger, String, Text, Integer, Boolean, DateTime, ForeignKey, CheckConstraint, Index
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Issue(Base):
    __tablename__ = "issues"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    workspace_id = Column(BigInteger, ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    status = Column(String(20), default="open")
    creator_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    assignee_name = Column(String(100))
    executor_name = Column(String(100))
    executor_type = Column(String(20))
    executor_note = Column(Text)
    related_files = Column(JSONB, default=[])
    evidence_note = Column(Text)
    root_cause = Column(Text)
    failed_attempts = Column(Text)
    final_solution = Column(Text)
    reusable = Column(Boolean, default=False)
    tags = Column(JSONB, default=[])
    activity_log = Column(JSONB, default=list)
    version = Column(Integer, default=1)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    tasks = relationship("Task", back_populates="issue", cascade="all, delete-orphan")

    __table_args__ = (
        CheckConstraint("status IN ('open', 'in_progress', 'resolved', 'archived')"),
        CheckConstraint("executor_type IN ('human', 'ai_window', 'role', 'tool')"),
        Index("idx_issues_workspace", "workspace_id"),
        Index("idx_issues_status", "status"),
        Index("idx_issues_creator", "creator_id"),
    )
