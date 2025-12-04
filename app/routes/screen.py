from fastapi import APIRouter, Depends, HTTPException, status
from app.core.auth import require_admin, require_theatre_admin
from app.models.theatre import Theatre
from app.models.screen import Screen
from app.schemes.screen import ScreenCreate
from sqlalchemy.orm import Session
from app.core.auth import get_db

router = APIRouter(prefix="/admin/screen", tags=["Screen"])

@router.post("/")
def create_screen(data: ScreenCreate, db: Session = Depends(get_db), current_user = Depends(require_admin)):
    
    # check if theatre exists
    theatre = db.query(Theatre).filter(Theatre.id == data.theatre_id).first()
    if not theatre:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Theatre not found"
        )
    screen = Screen(name = data.name, theatre_id = data.theatre_id, total_seats = data.total_seats)
    db.add(screen)
    db.commit()
    db.refresh(screen)
    return screen

    