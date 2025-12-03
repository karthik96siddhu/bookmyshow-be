from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from app.db.database import SessionLocal
from app.models.user import User
from app.schemes.user import UserCreate, UserOut
from app.core.security import hash_password, verify_password, create_access_token, JWT_SECRET, JWT_ALGORITHM
from app.schemes.user import UserLogin
from app.core.auth import get_db, get_current_user

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


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

@router.post("/login")
def login_user(user_data: UserLogin, db: Session = Depends(get_db)):
    
    # check if user exists
    user = db.query(User).filter(User.email == user_data.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # verify password
    if not verify_password(user_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    # cretae JWT token
    token = create_access_token({"sub": str(user.id)})
    
    #return token + user info
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role
        }
    }
    
@router.get("/me", response_model=UserOut)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    return current_user
    

