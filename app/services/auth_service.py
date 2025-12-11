from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from app.core.config import get_settings
from typing import Optional
from app.models.user import User

settings = get_settings()

# Config
SECRET_KEY = settings.SECRET_KEY
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
ALGORITHM = settings.ALGORITHM

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def authenticate_user(db, useremail: str, password: str):
    user = get_user(db, useremail)
    if not user:
        return {
            "success": False,
            "message": "Invalid user!"
        }
    
    stored_hash = user.password
    if not verify_password(password, stored_hash):
        return {
            "success": False,
            "message": "Invalid password!"
        }
    return {
        "success": True,
        "data": user
    }

def verify_password(password: str, hashed_password) -> bool:
    return pwd_context.verify(password, hashed_password)

def get_user(db, useremail: str):
    user = db.query(User).filter(User.email == useremail, User.deleted_at.is_(None)).first()
    return user