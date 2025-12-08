from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.auth import get_db
from app.db.database import SessionLocal
from app.models.theatre import Theatre
from app.models.movie import Movie
from app.models.show import Show
from app.models.screen import Screen

router = APIRouter(prefix="/user-movies", tags=["User - Movies"])

@router.get("/{city}")
def list_movies_by_city(city: str, db: Session = Depends(get_db)):
    
    # select movies that have shows in the given city
    movies = (
        db.query(Movie)
        .join(Show, Show.movie_id == Movie.id)
        .join(Theatre, Theatre.id == Show.theatre_id)
        .filter(Theatre.city == city)
        .distinct()
        .all()
    )
    
    return movies

@router.get("/{city}/{movie_id}")
def list_theatres_for_movie(city: str, movie_id: int, db: Session = Depends(get_db)):
    
    #Query all shows of the movie in the given city
    shows = (
        db.query(Show)
        .join(Theatre, Theatre.id == Show.theatre_id)
        .filter(Show.movie_id == movie_id, Theatre.city == city)
        .all()
    )
    
    if not shows:
        return []
    
    # Group shows by theatre
    theatres_map = {}
    
    for show in shows:
        theatre = show.theatre # relationship from Show model
        if theatre.id not in theatres_map:
            theatres_map[theatre.id] = {
                "theatre_id": theatre.id,
                "name": theatre.name,
                "address": theatre.address,
                "shows": []
            }
        
        theatres_map[theatre.id]["shows"].append({
            "show_id": show.id,
            "screen_id": show.screen_id,
            "start_time": show.start_time,
            "base_price": show.base_price
        })
    
    return list(theatres_map.values())
