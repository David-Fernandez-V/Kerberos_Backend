import json
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi import HTTPException

from src.models.user_model import ChangeNameRequest, User, UserCreate, UserRequest, UserOut
from src.email_sistem.verify_email import send_verification_email
from src.services.auth_service import create_verification_token
from src.services.ws_manager import sidebar_manager

pwd_context = CryptContext(schemes=["bcrypt"])

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

#Modificar
def change_password(db: Session, user_id: int, new_password: str):
    user = db.query(User).filter(User.deleted == False, User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    hashed_password = pwd_context.hash(new_password)
    user.password_hash = hashed_password
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": f"Contraseña actualizada para el correo: {user.email}"}

async def change_name(db: Session, user: User, request: ChangeNameRequest):
    user_query = db.query(User).filter(User.deleted == False, User.id == user.id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    user_query.name = request.new_name
    db.add(user_query)
    db.commit()
    db.refresh(user)

    await sidebar_manager.broadcast(json.dumps({
        "type": "username",
    }))

    return {"message:": f"Nombre modificado correctamente"}

def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.deleted == False, User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    user.deleted = True
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message:": f"Usuario eliminado correctamente: {user.email}"}

def destroy_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db.delete(user)
    db.commit()
    return {"message:": f"Usuario eliminado correctamente: {user.email}"}

def check_master_password(user: User, request: UserRequest):
    if not pwd_context.verify(request.master_password, user.password_hash):
        raise HTTPException(status_code=401, detail="Contraseña maestra incorrecta")
    
    return {"message": f"Contraseña correcta"}
        