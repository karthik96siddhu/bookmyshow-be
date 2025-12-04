from pydantic import BaseModel

class TheaterCreate(BaseModel):
    name: str
    city: str
    address: str
    
class TheaterOut(BaseModel):
    id: int
    name: str
    city: str
    address: str
    
    class Config:
        orm_mode = True
        
