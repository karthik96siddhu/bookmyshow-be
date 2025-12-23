from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from datetime import datetime
from app.db.database import Base

class Payment(Base):
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    provider = Column(String(50), nullable=False)
    provider_payment_id = Column(String(100), nullable=True)
    status = Column(String(20), nullable=False) # INITIATED | SUCCESS | FAILED
    created_at = Column(DateTime, default=datetime.utcnow)
    