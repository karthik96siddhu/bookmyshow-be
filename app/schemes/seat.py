from pydantic import BaseModel

class SeatCreate(BaseModel):
    screen_id: int
    row: str
    seats_per_row: int
    
class SeatOut(BaseModel):
    id: int
    screen_id: int
    row: str
    seat_number: int
    seat_code: str
    
    class Config:
        orm_mode = True

