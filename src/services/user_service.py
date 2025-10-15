import os
import json
from jose import ExpiredSignatureError
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi import HTTPException
from jose import jwt

from src.email_sistem.confirmation_change_email import send_confirmation_change_email
from src.email_sistem.changemail_email import send_changemail_email
from src.models.user_model import ChangeNameRequest, ChangeEmailRequest, ChangePasswordRequest, User, UserCreate, UserRequest, UserOut
from src.email_sistem.verify_email import send_verification_email
from src.services.auth_service import create_verification_token
from src.services.ws_manager import sidebar_manager

pwd_context = CryptContext(schemes=["bcrypt"])

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

def create_user(db: Session, user_data: UserCreate):
    # Verificar si ya existe
    existing = db.query(User).filter(User.email == user_data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Correo ya registrado")

    # Hashear contraseña
    hashed_password = pwd_context.hash(user_data.password)
    new_user = User(
        email=user_data.email,
        password_hash=hashed_password,
        name=user_data.name,
        is_verified=False,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Generar token de verificación
    token = create_verification_token(new_user.email)

    # Enviar correo de verificación
    try:
        send_verification_email(new_user.email, token)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error enviando correo: {str(e)}")

    return {"message": f"Usuario registrado con éxito: {new_user.email}. Revisa tu correo para verificar la cuenta."}

def get_profile(user: User):
    me = UserOut(
        email=user.email,
        name=user.name
    )
    return me

async def change_password(db: Session, user: User, request: ChangePasswordRequest):
    user = db.query(User).filter(User.deleted == False, User.id == user.id).first()

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    if not pwd_context.verify(request.master_password, user.password_hash):
        raise HTTPException(status_code=401, detail="Contraseña maestra incorrecta")

    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    hashed_password = pwd_context.hash(request.new_password)
    user.password_hash = hashed_password

    db.add(user)
    db.commit()
    db.refresh(user)

    await sidebar_manager.send_to_user(user.id, json.dumps({
        "type": "logout",
    }))

    return {"message": f"Contraseña actualizada correctamente"}

async def change_name(db: Session, user: User, request: ChangeNameRequest):
    user_query = db.query(User).filter(User.deleted == False, User.id == user.id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    user_query.name = request.new_name
    db.add(user_query)
    db.commit()
    db.refresh(user)

    await sidebar_manager.send_to_user(user.id, json.dumps({
        "type": "username",
    }))

    return {"message:": f"Nombre modificado correctamente"}

async def change_email(db: Session, user: User, token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        new_email = payload.get("sub")

        if not new_email:
            raise HTTPException(status_code=400, detail="Token inválido")

        user_query = db.query(User).filter(User.deleted == False, User.id == user.id).first()

        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        if user.email == new_email:
            raise HTTPException(status_code=500, detail="El correo ya está verificado")       
    
        user_query.email = new_email
        db.commit()

        # Enviar correo de confrimación
        try:
            send_confirmation_change_email(new_email)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error enviando correo: {str(e)}")
        
        await sidebar_manager.send_to_user(user.id, json.dumps({
            "type": "logout",
        }))

        return {"message": "Correo modificado correctamente."}
    
    except ExpiredSignatureError:
        raise HTTPException(status_code=400, detail="El token ha expirado")

def request_email_change(user: User, request: ChangeEmailRequest):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    if not pwd_context.verify(request.master_password, user.password_hash):
        raise HTTPException(status_code=401, detail="Contraseña maestra incorrecta")

     # Generar token de verificación
    token = create_verification_token(request.new_email)

    # Enviar correo de cambio
    try:
        send_changemail_email(request.new_email, token)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error enviando correo: {str(e)}")

    return {"message": f"Solicitando cambio de correo a {request.new_email}. Revisa tu correo para verificar la cuenta."}

def check_master_password(user: User, request: UserRequest):
    if not pwd_context.verify(request.master_password, user.password_hash):
        raise HTTPException(status_code=401, detail="Contraseña maestra incorrecta")
    
    return {"message": f"Contraseña correcta"}
        