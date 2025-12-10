from fastapi import APIRouter, Depends, HTTPException
from app.core.auth import require_admin
from app.core.auth import get_db
from sqlalchemy.orm import Session
from app.models.seat import Seat
from app.schemes.seat import SeatCreate, SeatOut

router = APIRouter(
    prefix="/admin/seats",
    tags=["Admin Seats"])

@router.post("/")
def create_seat(data: SeatCreate, db: Session = Depends(get_db), current_user = Depends(require_admin)):
    screen = db.query(Seat).filter(Seat.id == data.screen_id).first()
    if not screen:
        HTTPException(status_code=404, detail="Screen not found")
    
    # Generate seats like A1, A2, ... B1, B2, ...
    seats = []
    
    for row_index in range(data.rows):
        row_leter = chr(ord("A")+ row_index)
        for seat_num in range(1, data.seats_per_row + 1):
            seat_code = f"{row_leter}{seat_num}"
            seat = Seat(
                screen_id=data.screen_id,
                row=row_leter,
                seat_number=seat_num,
                seat_code=seat_code
            )
            db.add(seat)
            seats.append(seat)
    
    db.commit()
    return {"message": "Seats generated", "total_seats": len(seats)}

