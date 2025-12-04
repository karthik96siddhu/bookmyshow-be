from pydantic import BaseModel

class MovieCreate(BaseModel):
    title: str
    language: str
    duration: int  # duration in minutes
    poster_url: str
    description: str 
    
class MovieOut(BaseModel):
    id: int
    title: str
    language: str
    duration: int
    poster_url: str
    description: str 
    
    class Config:
        orm_mode = True

