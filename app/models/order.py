from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from datetime import datetime
from app.db.database import Base

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    show_id = Column(Integer, ForeignKey("shows.id"), nullable=False)
    
    status = Column(String(20), nullable=False, default="PENDING")
    # PENDING | PAID | CANCELLED | FAILED
    payment_reference = Column(String, nullable=True)
    payment_provider = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    