from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.models.user import User
from app.schemes.user import UserCreate, UserOut
from app.core.security import hash_password

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

# Depends to get DB session
def get_db():
    db =SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=UserOut)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    print("Password received:", user_data.password, type(user_data.password))

    
    # Hash the password
    hashed_password = hash_password(user_data.password)
    
    # create User object
    new_user = User(
        name = user_data.name,
        email = user_data.email,
        password_hash = hashed_password,
        role = "user"
    )
    
    # save to DB
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

