from fastapi import APIRouter, Depends, HTTPException, status
from app.core.auth import require_admin
from app.models.theatre import Theatre
from app.models.screen import Screen
from app.models.movie import Movie
from app.models.show import Show
from app.schemes.show import ShowCreate, ShowOut
from sqlalchemy.orm import Session
from app.core.auth import get_db

router = APIRouter(prefix="/admin/show", tags=["Admin - Show"])

@router.post("/", response_model=ShowOut)
def create_show(data: ShowCreate, db: Session = Depends(get_db), current_user = Depends(require_admin)):
    
    # check if Movie exists
    movie = db.query(Movie).filter(Movie.id == data.movie_id).first()
    if not movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movie not found"
        )
    
    # check if theatre exists
    theatre = db.query(Theatre).filter(Theatre.id == data.theatre_id).first()
    if not theatre:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Theatre not found"
        )
    
    # check if screen exists
    screen = db.query(Screen).filter(Screen.id == data.screen_id).first()
    if not screen:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Screen not found"
        )
    
    # check if screen belongs to theatre
    if screen.theatre_id != theatre.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Screen does not belong to the specified theatre"
        )
    
    show = Show(
        movie_id = data.movie_id,
        theatre_id = data.theatre_id,
        screen_id = data.screen_id,
        start_time = data.start_time,
        base_price = data.base_price
    )
    
    db.add(show)
    db.commit()
    db.refresh(show)
    return show

    