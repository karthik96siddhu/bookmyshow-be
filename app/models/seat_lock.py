# tempararily locking seats during the booking process
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from datetime import datetime, timedelta
from app.db.database import Base

class SeatLock(Base):
    __tablename__ = "seat_locks"
    
    id= Column(Integer, primary_key=True, index=True)
    show_id = Column(Integer, ForeignKey("shows.id"), nullable=False)
    seat_id = Column(Integer, ForeignKey("seats.id"), nullable=False)
    locked_until = Column(DateTime, nullable=False, default=datetime.utcnow)
    user_id = Column(Integer, nullable=False)
    

# later we will update this to auto-exiry old locks


