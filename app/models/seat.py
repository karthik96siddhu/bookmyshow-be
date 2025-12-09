from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class Seat(Base):
    __tablename__ = "seats"
    
    id = Column(Integer, primary_key=True, index=True)
    screen_id = Column(Integer, ForeignKey("screens.id"), nullable=False)
    
    row = Column(String(5), nullabble=False)
    seat_number = Column(Integer, nullable=False)
    seat_code = Column(String(10), nullable=False)
    
    screen = relationship("Screen", back_populates="seats")

