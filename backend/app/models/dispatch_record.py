from sqlalchemy import Column, BigInteger, String, Text, Integer, Boolean, DateTime, ForeignKey, Index
from sqlalchemy.sql import func
from app.database import Base


class DispatchRecord(Base):
    __tablename__ = "dispatch_records"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    task_id = Column(BigInteger, ForeignKey("tasks.id"))
    ai_tool = Column(String(50), nullable=False)
    dispatch_reason = Column(Text)
    risk_level = Column(String(20))
    execution_prompt = Column(Text)
    execution_result = Column(Text)
    duration_seconds = Column(Integer)
    success = Column(Boolean)
    created_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        Index("idx_dispatch_task", "task_id"),
        Index("idx_dispatch_ai_tool", "ai_tool"),
    )
