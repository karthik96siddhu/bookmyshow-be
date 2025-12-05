from fastapi import APIRouter, Depends
from app.core.auth import require_admin
from app.models.theatre import Theatre
from app.schemes.theatre import TheatreCreate
from sqlalchemy.orm import Session
from app.core.auth import get_db

router = APIRouter(prefix="/admin/theatre", tags=["Admin - Theatre"])

@router.post("/")
def create_theatre(data: TheatreCreate, db: Session = Depends(get_db), current_user = Depends(require_admin)):
    theatre = Theatre(name = data.name, city= data.city, address = data.address)
    db.add(theatre)
    db.commit()
    db.refresh(theatre)
    return theatre