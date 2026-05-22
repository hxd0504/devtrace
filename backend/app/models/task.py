from sqlalchemy import Column, BigInteger, String, Text, Integer, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    issue_id = Column(BigInteger, ForeignKey("issues.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    status = Column(String(20), default="todo")
    owner_name = Column(String(100))
    executor_name = Column(String(100))
    executor_type = Column(String(20))
    executor_note = Column(Text)
    related_files = Column(JSONB, default=list)
    evidence_source = Column(Text)
    evidence_summary = Column(Text)
    acceptance_criteria = Column(Text)
    risk_level = Column(String(20))
    activity_log = Column(JSONB, default=list)
    version = Column(Integer, default=1)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    issue = relationship("Issue", back_populates="tasks")

    __table_args__ = (
        CheckConstraint("status IN ('todo', 'doing', 'done')"),
        CheckConstraint("executor_type IN ('human', 'ai_window', 'role', 'tool')"),
        CheckConstraint("risk_level IN ('low', 'medium', 'high')"),
    )
