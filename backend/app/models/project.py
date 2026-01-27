from sqlalchemy import Column, String, DateTime, Text, ForeignKey, Integer
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from app.database import Base

class Project(Base):
    __tablename__ = "projects"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    template = Column(String, nullable=True)  # basic, experiment, survey, se, custom
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    papers = relationship("Paper", back_populates="project", cascade="all, delete-orphan")
    columns = relationship("ColumnDef", back_populates="project", cascade="all, delete-orphan")
