from fastapi import HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from src.models.user_model import User
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta, timezone
from jose.exceptions import ExpiredSignatureError
import os
from dotenv import load_dotenv

#from src.email_sistem.confirmation_email import send_confirmation_email
from src.sendgrid_sistem.send_confirmation import send_confirmation_email

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(hours=1))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def authenticate_user(db: Session, email: str, password: str):
    auth_user = db.query(User).filter(User.email == email, User.deleted == False, User.is_verified == True).first()
    if not auth_user or not pwd_context.verify(password, auth_user.password_hash):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas.")
    token = create_access_token(data={"sub": auth_user.email})
    
    response = JSONResponse(content={"message": "Login exitoso"})

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=True,  #Cambiar a false para pruebas en Locust
        samesite="none",
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
        secure=True,
        samesite="none",
        max_age=900,
        expires=900,
        path="/"
    )
    return response

#Registro

def create_verification_token(email: str):
    expire = datetime.now(timezone.utc) + timedelta(hours=1)
    payload = {"sub": email, "exp": expire, "type": "verification"}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_verification_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "verification":
            return None
        return payload.get("sub")  # devuelve el email
    except Exception:
        return None

def verify_email(db: Session, token: str):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")

        if not email:
            raise HTTPException(status_code=400, detail="Token inválido o expirado")

        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        if user.is_verified:
            raise HTTPException(status_code=500, detail="El correo ya está verificado")

        user.is_verified = True
        db.commit()

        # Enviar correo de confrimación
        try:
            send_confirmation_email(email)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error enviando correo: {str(e)}")

        return {"message": "Correo verificado con éxito"}
    
    except ExpiredSignatureError:
        # token vencido
        email = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_exp": False}).get("sub")
        if email:
            user = db.query(User).filter(User.email == email, User.is_verified == False).first()
            if user:
                db.delete(user)
                db.commit()
        raise HTTPException(status_code=400, detail="El token ha expirado, vuelve a registrarte")
