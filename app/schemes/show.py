from pydantic import BaseModel
from datetime import datetime

class ShowCreate(BaseModel):
    movie_id: int
    theatre_id: int
    screen_id: int
    start_time: datetime
    base_price: int
    
class ShowOut(BaseModel):
    id: int
    movie_id: int
    theatre_id: int
    screen_id: int
    start_time: datetime
    base_price: int
    
    class Config:
        orm_mode = True


    