from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.db.database import SessionLocal
from app.core.auth import get_db
from app.models.show import Show
from app.models.screen import Screen
from app.models.seat import Seat
from app.models.booking import Booking
from app.models.seat_lock import SeatLock

router = APIRouter(
    prefix="/shows",
    tags=["User - Seat Map"]
)

@router.get("/{show_id}/seat-map")
def get_seat_map(show_id: int, db: Session = Depends(get_db)):
    
    # Validate Show
    show = db.query(Show).filter(Show.id == show_id).first()
    
    if not show:
        return HTTPException(status_code=404, detail="Show not found")

    screen_id = show.screen_id
    
    # fetch seats from the screen
    seats = db.query(Seat).filter(Seat.screen_id == screen_id).all()
    
    # fetch booked seats for this show
    booked = db.query(Booking.seat_id).filter(Booking.show_id == show_id).all()
    booked_seat_ids = {b[0] for b in booked}
    
    # fetch active locks (not expired)
    locks = db.query(SeatLock).filter(
        SeatLock.show_id == show_id,
        SeatLock.locked_until > datetime.utcnow()
    ).all()
    locked_seat_ids = {l.seat_id for l in locks}
    
    # Build response
    seat_map = []
    for seat in seats:
        status = "available"
        if seat.id in booked_seat_ids:
            status = "booked"
        elif seat.id in locked_seat_ids:
            status = "locked"
        
        seat_map.append({
            "seat_id": seat.id,
            "row": seat.row,
            "code": seat.seat_code,
            "number": seat.seat_number,
            "status":status
        })
        
    return {
        "sreen_id": screen_id,
        "show_id": show_id,
        "seats": seat_map
    }

    