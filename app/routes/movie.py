from fastapi import APIRouter, Depends, HTTPException, status
from app.core.auth import require_admin, require_theatre_admin
from app.models.theatre import Theatre
from app.models.movie import Movie
from app.schemes.movie import MovieCreate
from sqlalchemy.orm import Session
from app.core.auth import get_db

router = APIRouter(prefix="/admin/movie", tags=["Admin - Movie"])

@router.post("/")
def create_screen(data: MovieCreate, db: Session = Depends(get_db), current_user = Depends(require_admin)):
    
    movie = Movie(title=data.title, 
                  duration=data.duration, 
                  language=data.language, poster_url=data.poster_url,
                  description=data.description)
    db.add(movie)
    db.commit()
    db.refresh(movie)
    return movie

