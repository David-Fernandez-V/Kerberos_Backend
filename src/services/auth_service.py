from fastapi import HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from src.models.user_model import User
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def authenticate_user(db: Session, email: str, password: str):
    auth_user = db.query(User).filter(User.email == email, User.deleted == False).first()
    if not auth_user or not pwd_context.verify(password, auth_user.password_hash):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas.")
    token = create_access_token(data={"sub": auth_user.email})
    
    response = JSONResponse(content={"message": "Login exitoso"})

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=False,  # importante en producción con HTTPS
        samesite="Lax",  # o "Strict", dependiendo de tu frontend/backend
        max_age=1800,
        expires=1800,
        path="/"
    )
    return response

def refresh_token(current_user: User):
    new_token = create_access_token(data={"sub": current_user.email})
    response = JSONResponse(content={"message": "Token renovado"})
    response.set_cookie(
        key="access_token",
        value=new_token,
        httponly=True,
        secure=False,
        samesite="Lax",
        max_age=900,
        expires=900,
        path="/"
    )
    return response
