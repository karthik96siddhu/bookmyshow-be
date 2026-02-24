from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt
from dotenv import load_dotenv
import os

load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
JWT_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", 60))


# Use bcrypt_sha256 so very long passwords are safe (bcrypt limits to 72 bytes).
# Keep "bcrypt" as a fallback so existing hashes remain verifiable.
# Prefer a backend without the 72-byte bcrypt limit for new hashes, but keep
# bcrypt variants as fallbacks to verify existing hashes.
pwd_context = CryptContext(schemes=["pbkdf2_sha256", "bcrypt_sha256", "bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    if password is None:
        raise ValueError("password must be provided")
    # Use the CryptContext to choose the best hashing scheme (we prefer
    # pbkdf2_sha256 so no bcrypt 72-byte limit applies to new hashes).
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # If the stored hash is a bcrypt-style hash, bcrypt backends may raise
    # when given inputs over 72 bytes. Truncate the input similarly to the
    # hashing side to ensure verification works against existing bcrypt hashes.
    if hashed_password and hashed_password.startswith("$2"):
        pw_bytes = plain_password.encode("utf-8")
        if len(pw_bytes) > 72:
            plain_password = pw_bytes[:72].decode("utf-8", errors="ignore")
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=JWT_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token

    