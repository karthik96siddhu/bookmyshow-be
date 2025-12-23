from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.auth import get_db
from app.models.order import Order
from app.models.booking import Booking
from app.models.show import Show
from app.models.seat_lock import SeatLock
from datetime import datetime

router = APIRouter(
    prefix="/orders",
    tags=["User - Orders"]
)

@router.post("/{show_id}/orders")
def create_order(show_id: int, user_id: int, db: Session = Depends(get_db)):
    
    order = Order(user_id=user_id, show_id=show_id, status="PENDING")
    db.add(order)
    db.commit()
    db.refresh(order)
    return {
        "order_id": order.id,
        "status": order.status
    }
    
@router.post("/orders/{order_id}/confirm")
def confirm_order(order_id: int, payment_reference: str, db: Session = Depends(get_db)):
    
    order = db.query(Order).filter(Order.id == order_id).first()
    
    if not order:
        return HTTPException(status_code=404, detail="Order not found")
    
    if order.status != "PENDING":
        return HTTPException(status_code=400, detail="Order already processed")
    
    now = datetime.utcnow()
    
    locks = db.query(SeatLock).filter(
        SeatLock.show_id == order.show_id,
        SeatLock.user_id == order.user_id,
        SeatLock.locked_until > now
    ).all()
    
    if not locks:
        raise HTTPException(status_code=400, detail="Seats locks expired")
    
    for lock in locks:
        booking = Booking(
            order_id=order.id,
            show_id=order.show_id,
            seat_id=lock.seat_id
        )
        db.add(booking)
        db.delete(lock)
    
    order.status = "PAID"
    order.payment_reference = payment_reference
    order.payment_provider = "RAZORPAY"  # Example provider
    
    db.commit()
    
    return {
        "message": "Booking confirmed",
        "order_id": order.id
    }

@router.post("/orders/{order_id}/cancel")
def cancel_order(order_id: int, db: Session = Depends(get_db)):
    
    # fetch order
    order = db. query(Order).filter(Order.id == order_id).first()
    if not order:
        return HTTPException(status_code=404, detail="Order not found")
    
    # only PENDING order can be cancelled
    if order.status != "PENDING":
        return HTTPException(status_code=400, detail=f"Cannot cancel order with status {order.status}")
    
    # release seat locks
    locks = db.query(SeatLock).filter(
        SeatLock.show_id == order.show_id,
        SeatLock.user_id == order.user_id
    ).all()
    
    for lock in locks:
        db.delete(lock)
        
    # update order status
    order.status = "CANCELLED"
    db.commit()
    
    return {
        "message": "Order cancelled and seats released",
        "order_id": order.id
    }