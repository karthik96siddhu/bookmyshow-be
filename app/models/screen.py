from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base

class Screen(Base):
    __tablename__ = "screens"
    
    id = Column(Integer, primary_key=True, index=True)
    theatre_id = Column(Integer, ForeignKey("theatres.id"), nullable=False)
    name = Column(String(100), nullable=False)
    total_seats = Column(Integer, nullable=False)
    
    # Relationship to theatre
    theatre = relationship("Theatre", back_populates="screens")
    
