from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.db.database import SessionLocal
from app.core.auth import get_db
from app.models.show import Show
from app.models.screen import Screen
from app.models.seat import Seat
from app.models.booking import Booking
from app.models.seat_lock import SeatLock
from app.schemes.seat_lock import LockSeatRequest
router = APIRouter(
    prefix="/shows",
    tags=["User - Seat Map"]
)

def cleanup_expired_locks(db: Session, show_id: int):
    now = datetime.utcnow()
    expired_locks = db.query(SeatLock).filter(
        SeatLock.show_id == show_id,
        SeatLock.locked_until <= now
    ).all()
    for lock in expired_locks:
        db.delete(lock)
    db.commit()


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


@router.post("/{show_id}/lock_seats")
def lock_seats(show_id: int, payload: LockSeatRequest, db: Session = Depends(get_db)):
    
    # Validate show
    show = db.query(Show).filter(Show.id == show_id).first()
    if not show:
        return HTTPException(status_code=404, detail="Show not found")
    cleanup_expired_locks(db, show_id)
    
    now = datetime.utcnow()
    lock_duration = timedelta(minutes=5)
    lock_expires = now + lock_duration
    
    locked_ids = []
    
    for seat_id in payload.seat_ids:
        
        # check ig seats exists
        seat = db.query(Seat).filter(Seat.id == seat_id).first()
        if not seat:
            raise HTTPException(status_code=404, detail=f"Seat ID {seat_id} not found")
        
        # check if already booked
        existing_booking = db.query(Booking).filter(
            Booking.show_id == show_id,
            Booking.seat_id == seat_id
        ).first()
        
        if existing_booking:
            raise HTTPException(status_code=400, detail=f"Seat ID {seat_id} is already booked")
        
        # check if locked by someone
        existing_lock = db.query(SeatLock).filter(
            SeatLock.show_id == show_id,
            SeatLock.seat_id == seat_id,
            SeatLock.locked_until > now
        ).first()
        
        if existing_lock:
            raise HTTPException(status_code=400, detail=f"Seat ID {seat_id} is already locked")
        
        # create new lock
        seat_lock = SeatLock(
            show_id=show_id,
            seat_id=seat_id,
            locked_until=lock_expires
        )
        
        db.add(seat_lock)
        locked_ids.append(seat_id)
    db.commit()
    
    return {
        "message": "Seats locked successfully",
        "locked_seat_ids": locked_ids,
        "locked_until": lock_expires.isoformat()
    }


@router.post("/{show_id}/book-seats")
def book_seats(show_id: int, payload: LockSeatRequest, db: Session = Depends(get_db)):
    
    # validate show
    show = db.query(Show).filter(Show.id == show_id).first()
    if not show:
        return HTTPException(status_code=404, detail="Show not found")
    
    now = datetime.utcnow()
    
    for seat_id in payload.seat_ids:
        
        # check active lock
        lock = db.query(SeatLock).filter(
            SeatLock.show_id == show_id,
            SeatLock.seat_id == seat_id,
            SeatLock.locked_until > now
        ).first()
        
        if not lock:
            raise HTTPException(status_code=400, detail=f"Seat ID {seat_id} is not locked or lock has expired")
        
        # double check seat is not booked
        existing_booking = db.query(Booking).filter(
            Booking.show_id == show_id,
            Booking.seat_id == seat_id
        ).first()

        if existing_booking:
            raise HTTPException(status_code=409, detail=f"Seat ID {seat_id} is already booked")

        # create booking
        booking = Booking(
            show_id = show_id,
            seat_id = seat_id
        )
        
        db.add(booking)
        
        # remove lock
        db.delete(lock)
    
    db.commit()
    
    return {
        "message": "Booking confirmed",
        "show_id": show_id,
        "booked_seat_ids": payload.seat_ids
    }
