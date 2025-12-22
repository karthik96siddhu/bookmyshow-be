from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.database import Base

class Booking(Base):
    __tablename__ = "bookings"
    
    id = Column(Integer, primary_key=True, index=True)
    show_id = Column(Integer, ForeignKey("shows.id"), nullable=False)
    seat_id = Column(Integer, ForeignKey("seats.id"), nullable=False)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
