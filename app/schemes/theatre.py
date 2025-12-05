from pydantic import BaseModel

class TheatreCreate(BaseModel):
    name: str
    city: str
    address: str
    
class TheatreOut(BaseModel):
    id: int
    name: str
    city: str
    address: str
    
    class Config:
        orm_mode = True
        
