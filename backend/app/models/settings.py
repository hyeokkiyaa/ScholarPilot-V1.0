from sqlalchemy import Column, String, Text
from app.database import Base

class Settings(Base):
    __tablename__ = "settings"
    
    key = Column(String, primary_key=True)
    value = Column(Text, nullable=True)
