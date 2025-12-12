from pydantic import BaseModel
from typing import List

class LockSeatRequest(BaseModel):
    seat_ids: List[int]

class LockSeatResponse(BaseModel):
    message: str
    locked_until: str
    locked_seat_ids: List[int]
