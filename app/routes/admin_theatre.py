from fastapi import APIRouter, Depends
from app.core.auth import require_admin
from app.models.theatre import Theatre
from app.schemes.theater import TheaterCreate
from sqlalchemy.orm import Session
from app.core.auth import get_db

router = APIRouter(prefix="/admin/theater", tags=["Admin"])

@router.post("/")
def create_theater(data: TheaterCreate, db: Session = Depends(get_db), current_user = Depends(require_admin)):
    theater = Theatre(name = data.name, city= data.city, address = data.address)
    db.add(theater)
    db.commit()
    db.refresh(theater)
    return theater