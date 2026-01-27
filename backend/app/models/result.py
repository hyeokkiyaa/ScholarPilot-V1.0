from sqlalchemy import Column, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from app.database import Base

class Result(Base):
    __tablename__ = "results"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    paper_id = Column(String, ForeignKey("papers.id"), nullable=False)
    column_id = Column(String, ForeignKey("columns.id"), nullable=False)
    value = Column(Text, nullable=True)
    status = Column(String, default="pending")  # pending, processing, done, error, skipped
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    paper = relationship("Paper", back_populates="results")
    column = relationship("ColumnDef")
