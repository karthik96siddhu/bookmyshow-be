from pydantic import BaseModel

class ScreenCreate(BaseModel):
    name: str
    theatre_id: int
    total_seats: int

class ScreenOut(BaseModel):
    id: int
    name: str
    theatre_id: int
    total_seats: int
    
    class Config:
        orm_mode = True

